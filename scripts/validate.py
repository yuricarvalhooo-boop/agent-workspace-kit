#!/usr/bin/env python3
"""Verifica estrutura, links e separação local. Não é uma auditoria completa de segredos."""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
]


def markdown_links(text):
    # Não interpreta exemplos dentro de blocos cercados como links do documento.
    text = re.sub(r"^```.*?^```[^\n]*$", "", text, flags=re.S | re.M)
    return re.findall(r"\]\(([^)]+)\)", text)


def validate(root):
    root = root.resolve()
    errors = []
    try:
        options = json.loads((root / "catalogs/options.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Catálogo inválido: {exc}"]
    if options.get("schema_version") != 1:
        errors.append("Versão desconhecida do catálogo.")
    for group in ("skills", "tools", "connectors"):
        ids = [x["id"] for x in options.get(group, [])]
        if len(ids) != len(set(ids)):
            errors.append(f"IDs duplicados: {group}")
    for item in options.get("skills", []):
        skill_id = item["id"]
        if not SKILL_NAME.fullmatch(skill_id) or len(skill_id) > 64:
            errors.append(f"Nome de skill inválido: {skill_id}")
        for key in ("path", "workflow"):
            target = root / item[key]
            if not target.resolve().is_relative_to(root) or not target.is_file():
                errors.append(f"Fonte ausente ou externa: {item[key]}")
        source = root / item["path"]
        if source.is_file() and source.resolve().is_relative_to(root):
            text = source.read_text(encoding="utf-8")
            if not re.match(r"\A---\s*\nname: " + re.escape(skill_id) + r"\ndescription: [^\n]+\n---", text):
                errors.append(f"Frontmatter inválido: {item['path']}")

    skipped = {".git", ".local", "workspace", "__pycache__", "node_modules"}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in skipped for part in relative.parts):
            continue
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f"Arquivo externo ao kit: {relative.as_posix()}")
            continue
        if path.suffix not in (".md", ".json", ".py"):
            continue
        text = path.read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            errors.append(f"Possível credencial: {relative.as_posix()}")
        if path.suffix == ".md":
            for raw in markdown_links(text):
                link = raw.strip().strip("<>").split(' "', 1)[0]
                if urlsplit(link).scheme or link.startswith("#"):
                    continue
                target = path.parent / unquote(link.split("#", 1)[0])
                if not target.resolve().is_relative_to(root) or not target.exists():
                    errors.append(f"Link local inválido: {relative.as_posix()} -> {link}")

    config_path = root / ".local/setup.json"
    if config_path.exists():
        if not config_path.resolve().is_relative_to(root):
            errors.append("Configuração aponta para fora do kit.")
        else:
            try:
                config = json.loads(config_path.read_text(encoding="utf-8"))
                known = {x["id"] for x in options["skills"]}
                if config.get("schema_version") != 1:
                    errors.append("Versão desconhecida da configuração.")
                if not set(config.get("skills", [])).issubset(known):
                    errors.append("Seleção contém skill desconhecida.")
            except (OSError, ValueError, TypeError):
                errors.append("Configuração local inválida.")

    git = shutil.which("git")
    if (root / ".git").exists() and git:
        result = subprocess.run(
            [git, "-C", str(root), "ls-files", "-z"],
            capture_output=True, check=False,
        )
        if result.returncode != 0:
            errors.append("Não foi possível verificar os arquivos versionados.")
        else:
            for encoded in result.stdout.split(b"\0"):
                if not encoded:
                    continue
                name = encoded.decode("utf-8")
                if name.split("/")[0] in ("workspace", ".local", ".agents", ".claude"):
                    errors.append(f"Arquivo local não deve ser versionado: {name}")
    return errors


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    try:
        errors = validate(ROOT)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors = [f"Validação interrompida: {exc}"]
    print(json.dumps({
        "status": "fail" if errors else "pass",
        "errors": errors,
        "limits": "Estrutura e padrões limitados; sem autenticação, auditoria integral ou prova de comportamento.",
    }, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

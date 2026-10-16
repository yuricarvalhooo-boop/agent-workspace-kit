#!/usr/bin/env python3
"""Configure escolhas locais. Sem --apply, apenas apresenta uma prévia."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def catalog(root):
    return json.loads((root / "catalogs/options.json").read_text(encoding="utf-8"))


def safe_target(root, relative):
    base = root.resolve()
    target = base / relative
    if not target.resolve().is_relative_to(base):
        raise ValueError(f"Destino fora do kit: {relative}")
    return target


def choices(values, available, label):
    unique = list(dict.fromkeys(values))
    invalid = set(unique) - set(available)
    if invalid:
        raise ValueError(f"{label} desconhecidos: {', '.join(sorted(invalid))}")
    return unique


def build_plan(root, agent, skill_ids=(), connector_ids=(), tool_ids=()):
    if agent not in ("codex", "claude", "both", "manual"):
        raise ValueError("Agente inválido.")
    options = catalog(root)
    skills = {item["id"]: item for item in options["skills"]}
    selected_skills = choices(skill_ids, skills, "Skills")
    selected_connectors = choices(connector_ids, [x["id"] for x in options["connectors"]], "Conectores")
    selected_tools = choices(tool_ids, [x["id"] for x in options["tools"]], "Ferramentas")
    config = {
        "schema_version": 1,
        "stage": "configured",
        "agent": agent,
        "skills": selected_skills,
        "tools": [{"id": item, "status": "selected-not-verified"} for item in selected_tools],
        "connectors": [{"id": item, "status": "selected", "access": "not-granted"} for item in selected_connectors],
    }
    plan = {".local/setup.json": json.dumps(config, ensure_ascii=False, indent=2) + "\n"}
    collections = {
        "context": "Contexto e escolhas confirmadas",
        "knowledge/projects": "Memórias de projetos",
        "knowledge/decisions": "Decisões",
        "knowledge/conversations": "Checkpoints",
        "knowledge/learning": "Propostas de aprendizado",
        "knowledge/roadmap": "Melhorias",
        "processes": "Processos",
        "people": "Pessoas e responsabilidades profissionais",
        "companies": "Organizações",
        "meetings": "Reuniões e entrevistas",
        "sources": "Fontes recebidas",
    }
    initial = {
        "workspace/START.md": "# Estado atual\n\n- Objetivo: a escolher.\n- Estado: escolhas registradas; capacidades ainda a verificar.\n- Próximo passo: registrar o primeiro objetivo e validar as escolhas.\n\n[Configuração](context/setup.md)\n",
        "workspace/context/setup.md": (root / "templates/setup.md").read_text(encoding="utf-8"),
    }
    for path, title in collections.items():
        initial[f"workspace/{path}/INDEX.md"] = f"# {title}\n\nNenhum registro ainda. Adicione uma linha com link relativo ao criar uma fonte.\n"
    # Notas do usuário nunca são substituídas numa repetição do configurador.
    for path, content in initial.items():
        if not safe_target(root, path).exists():
            plan[path] = content

    surfaces = []
    if agent in ("codex", "both"):
        surfaces.append(".agents")
    if agent in ("claude", "both"):
        surfaces.append(".claude")
    for skill_id in selected_skills:
        source_path = skills[skill_id]["path"]
        source = safe_target(root, source_path).read_text(encoding="utf-8")
        frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", source, re.S)
        if not frontmatter:
            raise ValueError(f"Frontmatter ausente: {source_path}")
        for surface in surfaces:
            path = f"{surface}/skills/{skill_id}/SKILL.md"
            plan[path] = (
                "---\n" + frontmatter.group(1) + "\n---\n\n# Entrada local\n\n"
                f"Leia a [skill canônica](../../../{source_path}) e siga suas instruções.\n"
                "Esta entrada serve à descoberta; contas e ferramentas dependem do ambiente.\n"
            )
    for relative in plan:
        safe_target(root, relative)
    return plan


def apply_plan(root, plan):
    # Confere tudo antes da primeira escrita; não sobrescreve conteúdo conflitante.
    pending = []
    for relative, content in plan.items():
        target = safe_target(root, relative)
        if target.exists():
            if not target.is_file() or target.read_text(encoding="utf-8") != content:
                raise ValueError(f"Arquivo existente preservado: {relative}. Revise a configuração manualmente.")
        else:
            pending.append((target, content))
    for target, content in pending:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="\n")
    return len(pending)


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    options = catalog(ROOT)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True, choices=("codex", "claude", "both", "manual"))
    parser.add_argument("--skills", nargs="*", default=[], choices=[x["id"] for x in options["skills"]])
    parser.add_argument("--connectors", nargs="*", default=[], choices=[x["id"] for x in options["connectors"]])
    parser.add_argument("--tools", nargs="*", default=[], choices=[x["id"] for x in options["tools"]])
    parser.add_argument("--apply", action="store_true", help="Criar apenas os arquivos da seleção revisada.")
    args = parser.parse_args(argv)
    try:
        plan = build_plan(ROOT, args.agent, args.skills, args.connectors, args.tools)
        print(json.dumps({
            "mode": "apply" if args.apply else "preview",
            "agent": args.agent,
            "skills": args.skills,
            "tools_selected_not_installed": args.tools,
            "connectors_selected_not_connected": args.connectors,
            "files": sorted(plan),
        }, ensure_ascii=False, indent=2))
        if args.apply:
            count = apply_plan(ROOT, plan)
            print(f"{count} arquivo(s) criado(s). Nenhuma instalação ou conexão executada.")
        else:
            print("Prévia: nenhum arquivo alterado. Use --apply somente após confirmar as escolhas.")
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Configuração interrompida: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

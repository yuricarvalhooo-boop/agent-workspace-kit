#!/usr/bin/env python3
"""Busca local em Markdown da área pessoal; não lê contas ou arquivos fora dela."""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c))


def search(root, query, limit=5):
    if limit < 1:
        raise ValueError("O limite deve ser positivo.")
    terms = list(dict.fromkeys(re.findall(r"[^\W_]+", normalize(query))))
    if not terms:
        raise ValueError("Informe ao menos um termo.")
    base = root.resolve()
    personal = base / "workspace"
    if not personal.exists():
        return []
    if not personal.resolve().is_relative_to(base):
        raise ValueError("A área pessoal aponta para fora do kit.")
    hits = []
    for path in sorted(personal.rglob("*.md")):
        if not path.is_file() or not path.resolve().is_relative_to(personal.resolve()):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            folded = normalize(line)
            if all(term in folded for term in terms):
                hits.append({
                    "path": path.relative_to(base).as_posix(),
                    "line": number,
                    "text": line[:600],
                })
    return hits[:limit]


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        result = search(ROOT, args.query, args.limit)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"Busca interrompida: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

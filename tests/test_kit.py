import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, SOURCE / "scripts" / f"{name}.py")
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


configure = module("configure")
search = module("search")
validate = module("validate")


class KitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workspace-kit-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "kit"
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(
            ".git", ".local", "workspace", ".agents", ".claude", "__pycache__"
        ))

    def test_clean_distribution_has_no_local_configuration(self):
        self.assertEqual(validate.validate(self.root), [])
        self.assertFalse((self.root / "workspace").exists())
        self.assertFalse((self.root / ".local").exists())
        self.assertFalse((self.root / ".agents").exists())

    def test_cli_preview_does_not_write(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        result = subprocess.run(
            [sys.executable, str(self.root / "scripts/configure.py"),
             "--agent", "both", "--skills", "retomar", "--connectors", "github"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        after = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob("*"))
        self.assertEqual(before, after)

    def test_selected_skills_only_and_connectors_are_not_connected(self):
        plan = configure.build_plan(self.root, "both", ["retomar"], ["github"], ["git"])
        configure.apply_plan(self.root, plan)
        for surface in (".agents", ".claude"):
            discovered = list((self.root / surface / "skills").glob("*/SKILL.md"))
            self.assertEqual([p.parent.name for p in discovered], ["retomar"])
        state = json.loads((self.root / ".local/setup.json").read_text(encoding="utf-8"))
        self.assertEqual(state["connectors"], [{"id": "github", "status": "selected", "access": "not-granted"}])
        self.assertEqual(state["tools"][0]["status"], "selected-not-verified")
        self.assertEqual(validate.validate(self.root), [])

    def test_empty_selection_is_supported(self):
        configure.apply_plan(self.root, configure.build_plan(self.root, "manual"))
        self.assertFalse((self.root / ".agents").exists())
        state = json.loads((self.root / ".local/setup.json").read_text(encoding="utf-8"))
        self.assertEqual(state["skills"], [])
        self.assertEqual(state["connectors"], [])

    def test_unknown_skill_is_rejected_without_writes(self):
        with self.assertRaises(ValueError):
            configure.build_plan(self.root, "codex", ["unknown"])
        self.assertFalse((self.root / ".local").exists())

    def test_conflict_preserves_existing_files_before_any_write(self):
        target = self.root / ".agents/skills/retomar/SKILL.md"
        target.parent.mkdir(parents=True)
        target.write_text("custom skill", encoding="utf-8")
        plan = configure.build_plan(self.root, "codex", ["retomar"])
        with self.assertRaises(ValueError):
            configure.apply_plan(self.root, plan)
        self.assertEqual(target.read_text(encoding="utf-8"), "custom skill")
        self.assertFalse((self.root / ".local").exists())
        self.assertFalse((self.root / "workspace").exists())

    def test_repeat_preserves_notes_and_is_idempotent(self):
        configure.apply_plan(self.root, configure.build_plan(self.root, "codex", ["retomar"]))
        note = self.root / "workspace/START.md"
        note.write_text("# Meu objetivo confirmado\n", encoding="utf-8")
        count = configure.apply_plan(self.root, configure.build_plan(self.root, "codex", ["retomar"]))
        self.assertEqual(count, 0)
        self.assertEqual(note.read_text(encoding="utf-8"), "# Meu objetivo confirmado\n")

    def test_search_only_personal_area_with_accents_and_limit(self):
        personal = self.root / "workspace/knowledge"
        personal.mkdir(parents=True)
        (personal / "note.md").write_text("Decisão confirmada\nDecisao proposta\n", encoding="utf-8")
        (self.root / "docs/not-personal.md").write_text("Decisão externa", encoding="utf-8")
        hits = search.search(self.root, "decisao", 1)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["line"], 1)
        self.assertTrue(hits[0]["path"].startswith("workspace/"))
        self.assertEqual(search.search(self.root, "nunca-existiu"), [])

    def test_broken_reference_is_reported(self):
        (self.root / "docs/bad.md").write_text("[Fonte](missing.md)", encoding="utf-8")
        self.assertTrue(any("missing.md" in error for error in validate.validate(self.root)))

    def test_credential_pattern_is_reported(self):
        (self.root / "docs/bad.md").write_text("gh" + "p_" + "a" * 36, encoding="utf-8")
        self.assertTrue(any("credencial" in error for error in validate.validate(self.root)))

    @unittest.skipUnless(shutil.which("git"), "Git é opcional")
    def test_local_data_are_ignored_and_forced_tracking_is_reported(self):
        def git(*args):
            return subprocess.run(
                ["git", "-C", str(self.root), *args],
                capture_output=True, check=True,
            )
        git("init", "-b", "main")
        configure.apply_plan(self.root, configure.build_plan(self.root, "both", ["retomar"]))
        for path in ("workspace/START.md", ".local/setup.json", ".agents/skills/retomar/SKILL.md",
                     ".claude/skills/retomar/SKILL.md"):
            git("check-ignore", path)
        git("add", ".")
        self.assertEqual(validate.validate(self.root), [])
        git("add", "-f", "workspace/START.md")
        self.assertTrue(any("workspace/START.md" in error for error in validate.validate(self.root)))


if __name__ == "__main__":
    unittest.main()

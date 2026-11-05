#!/usr/bin/env python3
"""Tests for antigravity support in nystack."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASH = r"C:\Program Files\Git\bin\bash.exe" if os.name == "nt" else "bash"

class TestAntigravitySupport(unittest.TestCase):
    def test_gemini_md_exists_and_references_agents(self):
        gemini_path = os.path.join(ROOT, "GEMINI.md")
        self.assertTrue(os.path.isfile(gemini_path), "GEMINI.md must exist")
        with open(gemini_path, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("@AGENTS.md", content, "GEMINI.md should reference @AGENTS.md")

    def test_install_script_syntax(self):
        install_script = os.path.join(ROOT, "scripts", "install.sh")
        result = subprocess.run([BASH, "-n", install_script], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"bash -n failed: {result.stderr}")

    def test_install_antigravity_flag(self):
        install_script = os.path.join(ROOT, "scripts", "install.sh")
        result = subprocess.run([BASH, install_script, "--antigravity", "--dry-run"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"install.sh failed: {result.stderr}")
        self.assertIn(".gemini/config/skills", result.stdout, "install.sh --antigravity should target .gemini/config/skills")
        self.assertIn(".claude/skills", result.stdout, "install.sh should always target .claude/skills")

    def test_install_agy_alias(self):
        install_script = os.path.join(ROOT, "scripts", "install.sh")
        result = subprocess.run([BASH, install_script, "--agy", "--dry-run"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"install.sh failed: {result.stderr}")
        self.assertIn(".gemini/config/skills", result.stdout, "install.sh --agy should target .gemini/config/skills")

    def test_validate_repo(self):
        validate_script = os.path.join(ROOT, "scripts", "validate.py")
        result = subprocess.run([sys.executable, validate_script], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"validate.py failed: {result.stdout}\n{result.stderr}")

if __name__ == "__main__":
    unittest.main()

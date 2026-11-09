import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_directory_archive_has_no_local_server_or_executable_files(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/package.py"), "--check", "--zip"], check=True)
        version = json.loads((ROOT / "plugin.json").read_text())["version"]
        with zipfile.ZipFile(ROOT / "dist" / f"ponko-claude-directory-{version}.zip") as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read("ponko/.claude-plugin/plugin.json"))
            self.assertNotIn("mcpServers", manifest)
            self.assertIn("ponko/skills/ponko/references/docs.md", names)
            self.assertIn("ponko/" + manifest["icon"].removeprefix("./"), names)
            self.assertFalse(any(name.endswith((".py", ".cjs")) or name.endswith("mcp.json")
                                 for name in names))

    def test_smoke_child_does_not_receive_installer_credentials(self):
        spec = importlib.util.spec_from_file_location("smoke", ROOT / "scripts/smoke_mcp.py")
        smoke = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(smoke)
        # Stop at the process boundary: inspect the actual environment the smoke
        # runner gives a child without touching the machine's games or secrets.
        class Captured(Exception):
            pass
        def capture(*args, **kwargs):
            self.assertTrue("PONKO_TEST_CREDENTIAL" not in kwargs["env"],
                            "Smoke runner forwarded the synthetic credential")
            self.assertIn("CRABBY_INSTANCES_DIR", kwargs["env"])
            raise Captured
        with patch.dict("os.environ", {"PONKO_TEST_CREDENTIAL": "synthetic-test-value"}):
            with patch.object(smoke.subprocess, "run", side_effect=capture):
                with self.assertRaises(Captured):
                    smoke.check(sys.executable, False)

    def test_launcher_reports_missing_configured_executable_on_stderr(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            launcher = ROOT / "scripts/launch-mcp.cjs"
            (root / "scripts/launch-mcp.cjs").write_bytes(launcher.read_bytes())
            (root / "mcp.json").write_text(json.dumps({"mcpServers": {
                "test": {"command": "ponko-test-nonexistent-binary", "args": []}}}))
            result = subprocess.run(["node", str(root / "scripts/launch-mcp.cjs")],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "")
            self.assertIn("ponko-test-nonexistent-binary", result.stderr)

    def test_launcher_preserves_stdio_and_child_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            (root / "scripts/launch-mcp.cjs").write_bytes((ROOT / "scripts/launch-mcp.cjs").read_bytes())
            (root / "mcp.json").write_text(json.dumps({"mcpServers": {
                "test": {"command": sys.executable, "args": ["-c",
                    "import sys; print(sys.stdin.readline().strip()); sys.exit(7)"]}}}))
            result = subprocess.run(["node", str(root / "scripts/launch-mcp.cjs")],
                                    input='{"jsonrpc":"2.0"}\n', capture_output=True, text=True)
            self.assertEqual(result.returncode, 7)
            self.assertEqual(result.stdout, '{"jsonrpc":"2.0"}\n')
            self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()

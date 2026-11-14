import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class DistributionTests(unittest.TestCase):
    def test_release_archive_contains_complete_root_plugin(self):
        subprocess.run([sys.executable, str(ROOT / "scripts/package.py"), "--check", "--zip"], check=True)
        version = json.loads((ROOT / "plugin.json").read_text())["version"]
        with zipfile.ZipFile(ROOT / "dist" / f"ponko-{version}.zip") as archive:
            names = archive.namelist()
            manifest = json.loads(archive.read("ponko/.claude-plugin/plugin.json"))
            self.assertIn("ponko/skills/ponko/references/docs.md", names)
            self.assertIn("ponko/" + manifest["icon"].removeprefix("./"), names)
            mcp = json.loads(archive.read("ponko/.mcp.json"))
            # The directory only accepts local MCP commands it can follow, so the
            # Claude entry runs the installed executable with no bundled script.
            portable = json.loads(archive.read("ponko/mcp.json"))
            self.assertEqual(mcp["mcpServers"], portable["mcpServers"])
            scripts = [n for n in names if n.endswith((".js", ".cjs", ".mjs", ".sh", ".py"))]
            self.assertEqual(scripts, [])

    def test_smoke_child_runs_with_an_isolated_environment(self):
        spec = importlib.util.spec_from_file_location("smoke", ROOT / "scripts/smoke_mcp.py")
        smoke = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(smoke)
        # Stop at the process boundary: inspect the actual environment the smoke
        # runner gives a child without touching the machine's games.
        class Captured(Exception):
            pass
        def capture(*args, **kwargs):
            self.assertNotIn("PONKO_TEST_MARKER", kwargs["env"],
                             "Smoke runner forwarded the parent environment")
            self.assertIn("CRABBY_INSTANCES_DIR", kwargs["env"])
            raise Captured
        with patch.dict("os.environ", {"PONKO_TEST_MARKER": "1"}):
            with patch.object(smoke.subprocess, "run", side_effect=capture):
                with self.assertRaises(Captured):
                    smoke.check(sys.executable, False)


if __name__ == "__main__":
    unittest.main()

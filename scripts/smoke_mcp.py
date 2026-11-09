#!/usr/bin/env python3
"""Exercise the real MCP stdio protocol against an isolated, empty registry."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def check(binary, read_only):
    plugin = json.loads((ROOT / "plugin.json").read_text())
    with tempfile.TemporaryDirectory(prefix="ponko-mcp-smoke-") as directory:
        env = {"HOME": directory, "LOCALAPPDATA": directory,
               "TMPDIR": directory, "TMP": directory, "TEMP": directory,
               "CRABBY_INSTANCES_DIR": str(Path(directory) / "instances")}
        messages = [
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": plugin["name"] + "-smoke", "version": plugin["version"]}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
                "name": "list_instances", "arguments": {}}},
        ]
        result = subprocess.run(
            [binary, *(["--read-only"] if read_only else [])],
            input="".join(json.dumps(message) + "\n" for message in messages),
            text=True, capture_output=True, timeout=30, env=env, cwd=directory,
            check=True,
        )
        replies = {reply["id"]: reply for line in result.stdout.splitlines()
                   if (reply := json.loads(line)).get("id") is not None}
        for message_id in (1, 2, 3):
            if "error" in replies[message_id]:
                raise RuntimeError(replies[message_id]["error"])
        assert replies[1]["result"]["serverInfo"]["name"] == "ponko-mcp"
        names = {tool["name"] for tool in replies[2]["result"]["tools"]}
        assert {"list_instances", "instance_info", "world_summary", "perf_report"} <= names
        assert ("launch" not in names) == read_only
        assert ("set_component" not in names) == read_only
        call = replies[3]["result"]
        assert not call.get("isError"), call
        content = next(item["text"] for item in call["content"] if item["type"] == "text")
        assert json.loads(content) == [], content
        print(f"{'Read-only' if read_only else 'Full'}: handshake, {len(names)} tools, empty discovery OK")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/smoke_mcp.py /absolute/path/to/ponko-mcp")
    executable = str(Path(sys.argv[1]).resolve(strict=True))
    check(executable, False)
    check(executable, True)

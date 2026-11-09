#!/usr/bin/env python3
"""Generate host adapters from the portable package; check drift or build a ZIP."""

import argparse
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def adapters():
    plugin = json.loads((ROOT / "plugin.json").read_text())
    servers = json.loads((ROOT / "mcp.json").read_text())["mcpServers"]
    identity = {key: plugin[key] for key in (
        "name", "version", "description", "author", "homepage", "repository",
        "license", "keywords",
    )}
    openai = plugin["extensions"]["com.openai"]
    return {
        ".claude-plugin/plugin.json": {**identity, "icon": "./assets/icon.png"},
        ".cursor-plugin/plugin.json": {**identity, "logo": "./assets/icon.png"},
        ".codex-plugin/plugin.json": {
            **identity, **openai, "skills": "./skills/", "mcpServers": "./configs/stdio.mcp.json",
        },
        ".mcp.json": {"mcpServers": {
            name: {"command": "node", "args": [
                "${CLAUDE_PLUGIN_ROOT}/scripts/launch-mcp.cjs", name,
            ]} for name in servers
        }},
        "configs/stdio.mcp.json": {"mcpServers": servers},
        "gemini-extension.json": {
            "name": plugin["name"], "version": plugin["version"],
            "description": plugin["description"], "mcpServers": servers,
            "contextFileName": "GEMINI.md",
        },
        ".claude-plugin/marketplace.json": {
            "name": "ponko-plugins", "owner": plugin["author"],
            "metadata": {"description": plugin["description"]},
            "plugins": [{"name": plugin["name"], "source": "./",
                         "description": plugin["description"]}],
        },
        ".agents/plugins/marketplace.json": {
            "name": "ponko-plugins", "interface": {"displayName": "Ponko Plugins"},
            "plugins": [{
                "name": plugin["name"],
                "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Developer Tools",
            }],
        },
        "configs/vscode.mcp.json": {"servers": servers},
        "configs/read-only.mcp.json": {"mcpServers": {
            name: {**server, "args": [*server.get("args", []), "--read-only"]}
            for name, server in servers.items()
        }},
    }



def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail on stale generated adapters")
    parser.add_argument("--zip", action="store_true", help="Also build dist/ponko-VERSION.zip")
    args = parser.parse_args()
    generated = adapters()
    stale = []
    for name, data in generated.items():
        path = ROOT / name
        expected = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            if not path.exists() or path.read_text() != expected:
                stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected)
    if stale:
        parser.exit(1, "Stale adapters: " + ", ".join(stale) + "\nRun python3 scripts/package.py\n")
    if args.zip:
        version = json.loads((ROOT / "plugin.json").read_text())["version"]
        output = ROOT / "dist" / f"ponko-{version}.zip"
        files = [ROOT / p for p in [
            "plugin.json", "mcp.json", "GEMINI.md", "README.md", "LICENSE",
            "MARKETPLACES.md", "scripts/launch-mcp.cjs", "assets/icon.png", *generated,
        ]]
        files.extend(sorted((ROOT / "skills").rglob("*.md")))
        output.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(files):
                archive.write(path, "ponko/" + path.relative_to(ROOT).as_posix())
        print(output)
    print("Host adapters are consistent." if args.check else "Generated host adapters.")


if __name__ == "__main__":
    main()

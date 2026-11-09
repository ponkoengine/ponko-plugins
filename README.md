# Ponko plugins

Connect **Codex, Claude Code, Cursor, Gemini CLI, and GitHub Copilot in VS Code**
to your local [Ponko Engine](https://github.com/ponkoengine/ponko) game.
Inspect entities and resources, debug a paused simulation, capture screenshots,
and profile frame costs using Ponko's existing MCP server.

One shared package provides the host-specific plugins. There is no provider API
wrapper, API key, or extra service to run: your coding agent starts `ponko-mcp`
over stdio. The MCP executable is `ponko-mcp`; engine control environment variables and
registry paths retain their legacy `CRABBY_*` / `.crabby` names.

## 1. Install the MCP executable

Install [Rust](https://rustup.rs), then:

```sh
cargo install --git https://github.com/ponkoengine/ponko --locked ponko_mcp
ponko-mcp --help
```

Ensure the agent can find `ponko-mcp` on PATH (usually `~/.cargo/bin`, or
`%USERPROFILE%\.cargo\bin` on Windows). Restart GUI apps after changing PATH.
If necessary, replace `command` in your installed MCP config with the absolute
path to the executable. Nothing in this package installs binaries automatically.

For local development from an engine checkout:

```sh
cargo install --path /absolute/path/to/ponko/crates/ponko_mcp --locked
```

Install the binary in the same environment as the agent and game. A remote SSH,
container, or WSL session needs its own installation and local game endpoint.

## Basic engine instructions and docs

The bundled `ponko` skill helps the agent start a game, choose relevant examples,
and consult documentation that matches your engine dependency. The
[documentation map](skills/ponko/references/docs.md) links to the official
getting-started guide, Rust API, ECS, systems, 3D, C/C++, MCP, and profiling docs.
For a first project, follow [Getting started](https://github.com/ponkoengine/ponko/blob/main/book/src/getting-started.md).
For existing projects, use the engine revision in your lockfile rather than
assuming public `main` describes your version. Runtime tool schemas and game
capabilities take precedence over examples in these workflows.

## 2. Install for your agent

The GitHub commands below require this repository to have been pushed. To try an
unpublished checkout, use the local installation paths instead. Install one
Ponko connection per host to avoid duplicate tool listings.

### Install skills with npx skills

With a Node.js version supported by the [skills CLI](https://github.com/vercel-labs/skills):

```sh
npx skills add ponkoengine/ponko-plugins
```

Choose your agents and skills interactively. To install just the basic engine
guidance for Codex, Claude Code, and Cursor:

```sh
npx skills add ponkoengine/ponko-plugins --skill ponko -a codex -a claude-code -a cursor
```

Add `-g` for a user-wide installation. A local checkout also works:

```sh
npx skills add /absolute/path/to/ponko-plugins
```

This installs **skills only**. It does not install `ponko-mcp` or register an MCP
connection. Complete step 1 and use your host's MCP-only instructions below for
runtime tools. Alternatively, install the full host plugin, which includes both
skills and MCP configuration; you do not need a second skills installation.

### Claude Code

In Claude Code:

```text
/plugin marketplace add ponkoengine/ponko-plugins
/plugin install ponko@ponko-plugins
```

Restart Claude Code, approve the MCP connection if prompted, and try
`/ponko:ponko-setup`, `/ponko:ponko-inspect`, or `/ponko:ponko-profile`.
The full Claude plugin uses a bundled Node.js launcher to start the executable
configured in `mcp.json`. Install Node.js for this route. Other hosts use the
portable MCP definition directly.

For the public Claude Directory submission, use this repository's root (`.`),
branch `main`. The same package includes all skills, docs, the icon, and the MCP
launcher. See [the submission instructions](MARKETPLACES.md#claude--anthropic).

For a local checkout, run this from your **game** project:

```sh
claude --plugin-dir /absolute/path/to/ponko-plugins
```

MCP-only alternative (no bundled skills):

```sh
claude mcp add --scope user ponko -- ponko-mcp
```

### Codex

Register the bundled marketplace:

```sh
codex plugin marketplace add ponkoengine/ponko-plugins
codex plugin add ponko@ponko-plugins
```

For a local checkout, replace the first command with:

```sh
codex plugin marketplace add /absolute/path/to/ponko-plugins
```

Restart your session and invoke `$ponko-setup`, `$ponko-inspect`, or
`$ponko-profile`. Use `$ponko` for general engine guidance and documentation. If your installed CLI does not expose `plugin add`, update it
or install Ponko from the configured source in the desktop Plugins Directory.
Local plugin support varies by client; see the
[official packaging guide](https://developers.openai.com/plugins/build/plugins).

MCP-only alternative:

```sh
codex mcp add ponko -- ponko-mcp
```

### Cursor

Clone this repository, then copy the **whole package**, including hidden files,
into Cursor's local plugin directory. On macOS/Linux, for a new installation:

```sh
git clone https://github.com/ponkoengine/ponko-plugins.git
mkdir -p ~/.cursor/plugins/local/ponko
cp -R ponko-plugins/. ~/.cursor/plugins/local/ponko/
rm -rf ~/.cursor/plugins/local/ponko/.git
```

The removal above only removes the copied Git metadata, not your source checkout.
For an unpublished checkout, copy from its absolute path instead of cloning.
Restart Cursor or run **Developer: Reload Window**, then verify Ponko under
**Customize**. Local imports must be allowed by your organization. Copy the
files rather than symlinking from another directory: Cursor skips external
symlink targets. Recopy the updated package when developing.

MCP-only alternative: merge the `mcpServers.ponko` entry from [configs/stdio.mcp.json](configs/stdio.mcp.json)
into your game's `.cursor/mcp.json`, preserving existing servers. This provides
tools without the bundled skills. See [Cursor plugins](https://cursor.com/docs/plugins).

### Gemini CLI

This repository is also a native Gemini extension:

```sh
gemini extensions install https://github.com/ponkoengine/ponko-plugins
```

For local development:

```sh
gemini extensions link /absolute/path/to/ponko-plugins
```

Review the extension permission prompt and restart Gemini CLI. The extension
registers the same MCP tools and loads [GEMINI.md](GEMINI.md), which links to
the shared workflows. See the [extension reference](https://geminicli.com/docs/extensions/reference/).

### GitHub Copilot in VS Code

Recent VS Code releases support portable Agent Plugins. Merge this setting into
your user settings, using the absolute local checkout path:

```json
{
  "chat.pluginLocations": {
    "/absolute/path/to/ponko-plugins": true
  }
}
```

Reload VS Code and use a Copilot agent session. See the
[plugin reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference).

For an MCP-only installation, merge the `servers.ponko` entry from
[configs/vscode.mcp.json](configs/vscode.mcp.json) into your game's
`.vscode/mcp.json`, preserving other entries. Use **MCP: List Servers** to start
Ponko and review the trust prompt. The workspace format uses `servers`, not
`mcpServers`.

### Other MCP clients

Use a **local stdio server** with command `ponko-mcp` and no arguments. Clients
using an `mcpServers` map can use [configs/stdio.mcp.json](configs/stdio.mcp.json) as a template. Each client
has its own config location and skill support; an MCP config alone adds tools.

## 3. Connect a game

From an engine checkout, for example:

```sh
CRABBY_CONTROL=1 cargo run --release --example boids
```

On PowerShell, use `$env:CRABBY_CONTROL = "1"` before `cargo run`. For your own
game, enable its Ponko control endpoint in the same way. Then ask your agent:

> Use Ponko to list running games and inspect my game's entities and resources.

Or ask it to launch a game, giving the **absolute Cargo project path**:

> Launch the boids example from /absolute/path/to/ponko, paused and headless,
> run 600 ticks, and inspect the entity counts.

The `launch` tool defaults to a paused, headless release build. For screenshots,
request a windowed game (`headless: false`). The game must implement headless
operation; the launch environment variable cannot add that feature to a game.
Reflected components/resources are visible to tools; unreflected data is not.

Every client sees the same per-user instance registry. Select the intended
instance explicitly when several games run. Agents can change live game state,
launch builds, write saves, and quit games through the full server.

For observation, use `ponko-mcp --read-only`; a config is provided at
[configs/read-only.mcp.json](configs/read-only.mcp.json). Merge its server entry
into the host's MCP config, or edit the installed plugin's server `args` and
reload. Do not install both variants under the same server name. This option
hides simulation-writing tools; it is not a filesystem sandbox and does not
disable every side effect (for example, captures and traces can write files).

## Package layout and maintenance

| Files | Purpose |
| --- | --- |
| `plugin.json`, `mcp.json` | Portable Agent Plugins package; canonical metadata and MCP config |
| `.claude-plugin/` | Claude Code manifest and self-hosted marketplace |
| `.codex-plugin/`, `.agents/plugins/` | Codex compatibility manifest and marketplace |
| `.cursor-plugin/` | Cursor manifest (uses portable `mcp.json`) |
| `.mcp.json`, `scripts/launch-mcp.cjs` | Claude's inspectable MCP entry point |
| `gemini-extension.json`, `GEMINI.md` | Gemini CLI extension |
| `skills/` | Shared engine guidance, setup, inspection, and profiling workflows |
| `configs/` | MCP-only and observation templates |

Edit the portable manifests and skills, then regenerate adapters. Python 3.10+
is needed only for repository maintenance, not plugin use:

```sh
python3 scripts/package.py
python3 -m unittest discover -s tests -v
python3 scripts/package.py --check --zip
claude plugin validate . --strict
python3 scripts/smoke_mcp.py /absolute/path/to/ponko-mcp
npx skills add . --list
```

The smoke check performs a real stdio MCP handshake, lists tools, and discovers
an empty temporary registry in full and read-only modes. It never connects to
your games. The ZIP is written to `dist/ponko-<version>.zip`; it contains the plugin
files, not the engine executable. Host UI discovery and a real game session
still need manual acceptance in each host.

The single release archive includes the full plugin and the official icon from
`https://ponko.dev/favicon.svg`, rasterized to a square PNG. Repository maintenance
and test scripts are excluded from the archive.

See [MARKETPLACES.md](MARKETPLACES.md) for public directory submission steps,
including the extra requirements for a local MCP server.

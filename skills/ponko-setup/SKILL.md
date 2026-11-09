---
name: ponko-setup
description: Connect a coding agent to a local Ponko Engine game through ponko-mcp, or diagnose missing tools and empty game discovery.
---

Use the plugin's configured MCP executable. Current Ponko uses `ponko-mcp`,
while engine control variables and registry paths retain their legacy names.
Consult [Ponko documentation](https://github.com/ponkoengine/ponko/blob/main/book/src/SUMMARY.md) for the engine version
in the user's project; the local checkout may predate the public main branch.

1. Check whether the host exposes the Ponko MCP tools. If the server cannot start,
   check `ponko-mcp --help` in the host's execution environment. Install from the
   public engine source when needed:

   ```sh
   cargo install --git https://github.com/ponkoengine/ponko --locked ponko_mcp
   ```

   The host must inherit the directory containing `ponko-mcp` on PATH, usually
   `~/.cargo/bin`. A GUI may need a restart or an absolute executable path in its
   MCP config. A remote/container host needs the binary and game on that machine.

2. Call `list_instances`. If no game appears, start the user's intended game with
   its control endpoint enabled, or use `launch` when launching is part of the
   task. Pass the game's **absolute Cargo project directory** as `cwd`; installed
   plugins may run from a cache directory. Do not infer the game from plugin cwd.

   ```sh
   CRABBY_CONTROL=1 cargo run --release --example boids
   ```

   This example runs from an engine checkout. To start paused, add
   `CRABBY_START_PAUSED=1`. `HEADLESS=1` works only for games that implement it.
   `launch` enables control and defaults to a headless, paused release build.

3. Select the intended game from discovery and pass its `instance` id in later
   calls, especially when several games are running. Confirm `instance_info`
   and `world_summary` before changing state.

If a manually started game is invisible, check that server and game use the same
OS user and registry (`CRABBY_INSTANCES_DIR`, otherwise `~/.crabby/instances` on
Unix or `%LOCALAPPDATA%/crabby/instances` on Windows). The server communicates
with local control endpoints; an ordinary cloud chat cannot reach this machine.

For an observation session, launch the MCP server with `--read-only`. It hides
simulation-writing tools but is not an OS sandbox: screenshots, traces, camera
controls, and file-writing inspection tools may remain available. Use the tool
schemas supplied by the connected server for supported arguments.

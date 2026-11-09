---
name: ponko
description: Build or modify games with Ponko Engine, find its official documentation and examples, and choose engine APIs that match the project's version.
---

Ponko is a code-first Rust game engine with C and C++ bindings. Use the
[documentation map](references/docs.md) to find the relevant guide and source
examples before choosing an unfamiliar engine API.

For an existing game, inspect its Cargo manifest/lockfile or native dependency
revision first. Prefer documentation and examples from that same engine
revision; public `main` and latest API documentation may differ from the user's
dependency. Follow project instructions and preserve the chosen language,
features, architecture, and assets.

For a new game, use the current getting-started guide: install its required
toolchain/system libraries, create a Cargo project, add the engine dependency,
and adapt the smallest relevant official example. Start with a runnable window
or the requested headless simulation before adding gameplay. Enable features
only when the game needs them. Do not copy stale crate names, dependency
versions, platform paths, or API signatures from another project.

Setup initializes the game; per-frame behavior and fixed-step simulation serve
different purposes. Consult the systems and simulation-clock guides when
deciding where gameplay belongs. Keep assets relative to the game's documented
asset root. Consult the C/C++ guide for its own build and ABI requirements.

For runtime evidence, use the installed MCP tools when available. Read their
advertised schemas and query the selected game's capabilities when supported
before assuming a subsystem, rendering mode, or reflected type is available.
The plugin can be installed without a running game; use source docs for coding
and report when runtime verification was unavailable.

Validate the requested behavior with the project's normal build/tests and a
small reproduction. Use a windowed run for visual work and comparable release
measurements for performance claims. The setup, inspection, and profiling
skills provide the corresponding MCP workflows; they do not replace the
engine's version-specific documentation.

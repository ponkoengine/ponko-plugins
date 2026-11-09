# Official Ponko documentation

The source guide is the reliable entry point while the project website is being
reconfigured. These links track public `main`; for an existing project, use its
engine tag/commit in place of `main`, or read the matching local engine checkout.
Use the project's lockfile to choose the matching version on docs.rs. Do not
assume latest docs describe an older dependency.

| Need | Official source |
| --- | --- |
| Overview and current setup | [README](https://github.com/ponkoengine/ponko#readme) |
| Guide contents | [Guide index](https://github.com/ponkoengine/ponko/blob/main/book/src/SUMMARY.md) |
| First game, toolchain, platform requirements | [Getting started](https://github.com/ponkoengine/ponko/blob/main/book/src/getting-started.md) |
| Rust API | [ponko on docs.rs](https://docs.rs/ponko/) |
| Runnable examples | [Examples](https://github.com/ponkoengine/ponko/tree/main/examples) |
| Entities and queries | [ECS](https://github.com/ponkoengine/ponko/blob/main/book/src/ecs.md) |
| Frame systems and fixed ticks | [Systems](https://github.com/ponkoengine/ponko/blob/main/book/src/systems.md), [simulation clock](https://github.com/ponkoengine/ponko/blob/main/book/src/sim-clock.md) |
| 3D and feature requirements | [3D guide](https://github.com/ponkoengine/ponko/blob/main/book/src/3d.md) |
| C and C++ setup | [Native guide](https://github.com/ponkoengine/ponko/blob/main/book/src/c-cpp.md) |
| Local agent tools and connection | [MCP guide](https://github.com/ponkoengine/ponko/blob/main/book/src/agents.md) |
| Endpoint and capabilities | [Control guide](https://github.com/ponkoengine/ponko/blob/main/book/src/control.md) |
| Exposing game state to tools | [Reflection](https://github.com/ponkoengine/ponko/blob/main/book/src/reflection.md) |
| Headless checks | [Headless guide](https://github.com/ponkoengine/ponko/blob/main/book/src/headless.md) |
| Measurement and tracing | [Profiling](https://github.com/ponkoengine/ponko/blob/main/book/src/profiling.md) |
| Supported contracts and known gaps | [Stability](https://github.com/ponkoengine/ponko/blob/main/STABILITY.md), [roadmap](https://github.com/ponkoengine/ponko/blob/main/ROADMAP.md) |

Read the relevant chapter and its linked examples rather than loading every
page. For a connected server, its live tool schemas and per-instance capability
response determine what the installed version supports. If a tool or docs page
does not exist in that version, inspect the matching source or report the gap.

---
name: ponko-inspect
description: Inspect or debug a running Ponko Engine game using MCP entity, resource, log, simulation, and screenshot tools.
---

Call `list_instances`, select the user's game, and use its `instance` id for all
calls. Start with `instance_info` and `world_summary`. Read the connected tool
schemas rather than assuming argument shapes from another engine version.
When available, query `instance_capabilities` for the selected game before
choosing tools; it reports supported modes, subsystems, and reflected schemas.
Use the [documentation map](https://github.com/ponkoengine/ponko/blob/main/book/src/SUMMARY.md) for engine API details.

Use `list_resources` and `get_resource` for game-wide state. Use `entity_stats`
for counts and distributions; use filtered, paged `list_entities` and
`get_entity` when specific component values are needed. Only reflected data is
visible: a missing component is not evidence that the game lacks it. Inspect the
game's reflection registrations when relevant.

For a reproducible simulation bug, use a paused instance and `run_ticks` or
`watch` when advancing the simulation is authorized by the task. Record tick,
seed, parameters, and observed state. Use `read_logs`, carrying `next` into
`since`, for incremental output. For transient behavior, subscribe to reflected
events before advancing ticks and collect them afterwards.

Treat component/resource edits, spawning, loading saves/scenes, advancing ticks,
relaunching, and quitting as changes to the user's game. Apply them only within
the requested task. A checkpoint made with `save_world` can help compare a
simulation experiment, but does not roll back external files or all side effects.
Do not stop other instances discovered in the shared registry.

For visual checks, use a windowed instance (`headless: false` when launching),
then `screenshot`. Headless simulation checks do not establish rendering
correctness. State whether findings came from live MCP evidence, source
inspection, or an untested hypothesis.

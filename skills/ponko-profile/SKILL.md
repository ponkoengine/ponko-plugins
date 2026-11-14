---
name: ponko-profile
description: Measure and diagnose Ponko Engine game performance with MCP reports, system timings, and frame traces.
---

Select the intended game with `list_instances` and pass `instance` explicitly.
Check `instance_info`, build mode, whether the simulation is paused, and whether
the game is headless. Release and debug results are not interchangeable.

Collect `perf_report` and `system_timings` before suggesting an optimization.
Compare CPU work, GPU time, display wait, pass costs, entity/triangle counts,
and the heaviest systems or meshes. When the server provides
`render_inspector.counts.state_changes` (pipelines, bind groups, vertex and
index buffers, draws for the last recorded frame), use it to tell recording
cost from shading cost; it is null in headless or 2D-only games. A large display wait alone does not identify
a slow gameplay system. A headless report cannot establish rendering cost.

Before comparing quality or performance, read
`render_inspector.quality_autotune` in `perf_report` when the server provides
it. If it is not null, the game lets the engine adjust render scale and shadow
resolution from GPU timings: record the active choices, pins, freeze state,
reason and recent decisions, and have the game freeze or disable it for a
controlled comparison so quality does not change mid-measurement. When GPU
timings are unavailable the engine makes no automatic changes; do not base
quality advice on CPU frame time as a stand-in for GPU cost.

For GPU memory questions, read `render_inspector.gpu_memory_bytes` in
`perf_report`: every texture and buffer the engine holds, by class (frame
targets, shadows, atlases, textures, meshes, ...), its `total`, and the
platform's own `adapter` figure where there is one. `assets.gpu` covers the
game's assets only; do not treat it as the whole footprint (it repeats the
engine's total as `all_gpu_memory_bytes`). When the server offers the
`gpu_allocations` parameter, pass `true` (or a count for the largest) to list
each render target, post-processing image, shadow map and buffer with its
label, size, format, samples, usage and bytes in
`render_inspector.gpu_allocations`; ask for it only when needed, as it can be
long. Compare totals across `set_graphics_quality` to measure what a preset
costs.

Use `record_trace` for hitches when the task calls for deeper measurement. Use
`perf_hud` and a screenshot for an on-screen report when useful. Both can affect
the session or write artifacts; keep them within the user's requested scope.

For before/after comparisons, hold camera, resolution, seed, workload, warmup,
build mode, and sample duration constant. Report measured numbers and those
conditions. If a target remains unmet, say how far the measured result is from
it. Do not replace a rendering measurement with a compiler check or headless
test, or claim an improvement based only on a code change.

Consult the version-matched profiling guide in the
[documentation map](https://github.com/ponkoengine/ponko/blob/main/book/src/SUMMARY.md) for detailed engine APIs.

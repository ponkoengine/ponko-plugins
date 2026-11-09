---
name: ponko-profile
description: Measure and diagnose Ponko Engine game performance with MCP reports, system timings, and frame traces.
---

Select the intended game with `list_instances` and pass `instance` explicitly.
Check `instance_info`, build mode, whether the simulation is paused, and whether
the game is headless. Release and debug results are not interchangeable.

Collect `perf_report` and `system_timings` before suggesting an optimization.
Compare CPU work, GPU time, display wait, pass costs, entity/triangle counts,
and the heaviest systems or meshes. A large display wait alone does not identify
a slow gameplay system. A headless report cannot establish rendering cost.

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

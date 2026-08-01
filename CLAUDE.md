# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A small simulation exploring a hypothesis about gene-culture co-evolution: a
population of individuals whose propensity to interact is driven by both
1-bit "genes" (under Wright-Fisher selection toward a biological optimum) and
1-bit "memes" (spread horizontally through contact, 10x faster than genetic
change). The full model — including which parts are dictated by the original
spec (`instruct.md`) vs. which are implementation choices — is documented in
`README.md`; read it before changing the model, since it explains *why* the
mechanics are shaped the way they are, not just what they do.

## Commands

```sh
uv sync              # install dependencies into .venv
uv run globalbrain   # run both experimental conditions and write evolution.png
```

There is no test suite, linter, or formatter configured yet.

## Architecture

`src/globalbrain/`:

- `model.py` — the core per-turn mechanics, all operating on a `Population`
  (two `(n_individuals, 100)` bit arrays: `genes`, `memes`):
  - `make_initial_population` — genes and memes both start all-zero; all
    later variation comes from mutation.
  - `fitness` / `genetic_step` — Gaussian stabilizing selection (peaked at
    `OPTIMUM = 20`) and Wright-Fisher resampling with mutation (the genetic
    replicator dynamic).
  - `memetic_step` — tiny per-locus meme mutation, then configuration-model
    contact matching where each meeting draws two independent random loci
    (one per direction) so each side catches its own random meme from the
    other, not a shared-locus swap (the memetic replicator dynamic).
- `experiment.py` — `run_condition` interleaves 10 `memetic_step` calls per
  `genetic_step` (skipping the memetic step entirely for the "biological
  evolution only" condition, so its memes never mutate or spread and stay at
  all-zero forever) and records per-turn stats into a `Trace`.
  `run_both_conditions` runs both conditions from the same all-zero initial
  population.
- `plotting.py` — renders the 2x2 figure (mean interactions and
  gene/meme-preferred interactions, one row per condition) from two `Trace`s.
  `make_figure(..., surface=...)` takes a background color, used to render
  both the default (`evolution.png`) and a themed (`evolution_bg.png`,
  `BG_COLOR` in `__init__.py` — sampled directly from `color.png.png`) copy.
  Left-column lines use the categorical blue; right-column lines are always
  black, distinguished by linestyle (solid genetic / dashed cultural) rather
  than hue. Plot labels say "cultural" rather than "memetic" for
  readability — that renaming is display-only; the underlying code keeps
  `memetic_step`/`meme_component` naming. Re-validate with the dataviz
  skill's palette validator before changing any series colors.
- `__init__.py` — `main()` wires the above together for the `globalbrain`
  console script, producing both PNGs.

Everything is vectorized with numpy; there's no per-individual object, no
class hierarchy, and no config file — parameters are keyword defaults on the
functions in `model.py` and `experiment.py`, changed directly in code.

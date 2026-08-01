"""Runs the two experimental conditions and records per-turn statistics."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .model import Population, genetic_step, make_initial_population, memetic_step

MEMETIC_STEPS_PER_GENERATION = 10


@dataclass
class Trace:
    mean_interactions: list[float] = field(default_factory=list)
    gene_component: list[float] = field(default_factory=list)
    meme_component: list[float] = field(default_factory=list)

    def record(self, pop: Population) -> None:
        self.mean_interactions.append(float(pop.interactions().mean()))
        self.gene_component.append(float(100.0 * pop.gene_fraction().mean()))
        self.meme_component.append(float(100.0 * pop.meme_fraction().mean()))


def run_condition(
    pop: Population,
    rng: np.random.Generator,
    n_generations: int,
    memetic_evolution: bool,
) -> Trace:
    """Run `n_generations` genetic generations, each preceded by
    MEMETIC_STEPS_PER_GENERATION memetic sub-steps (skipped entirely when
    `memetic_evolution` is False, so memes stay at their initial values).
    Records one data point per turn, where a turn is one memetic sub-step.
    """
    trace = Trace()
    for _ in range(n_generations):
        for _ in range(MEMETIC_STEPS_PER_GENERATION):
            if memetic_evolution:
                pop = memetic_step(pop, rng)
            trace.record(pop)
        pop = genetic_step(pop, rng)
    return trace


def run_both_conditions(
    n_individuals: int = 300,
    n_generations: int = 600,
    seed: int = 0,
) -> tuple[Trace, Trace]:
    """Runs the 'biological evolution only' (memetic step skipped, so memes
    stay at all-zero forever) and 'biological + memetic evolution' (memes
    mutate and spread via contact) conditions, both starting from the same
    all-zero genes and memes."""
    initial = make_initial_population(n_individuals)

    bio_only = run_condition(
        Population(genes=initial.genes.copy(), memes=initial.memes.copy()),
        np.random.default_rng(seed + 1),
        n_generations,
        memetic_evolution=False,
    )
    bio_and_memetic = run_condition(
        Population(genes=initial.genes.copy(), memes=initial.memes.copy()),
        np.random.default_rng(seed + 2),
        n_generations,
        memetic_evolution=True,
    )
    return bio_only, bio_and_memetic

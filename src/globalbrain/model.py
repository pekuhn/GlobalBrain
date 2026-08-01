"""Core state and update rules for the gene-meme co-evolution model.

An individual carries two bit-strings of length ``n_loci`` each: genes and
memes. The number of interactions an individual makes per turn is a linear
function of how many of its gene bits and meme bits are set to 1, ranging
from ~0 (all zeros) to 200 (all ones), with genes and memes each
contributing half of the range.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

N_LOCI = 100
MAX_INTERACTIONS = 200
OPTIMUM = 20.0


@dataclass
class Population:
    genes: np.ndarray  # shape (n, N_LOCI), dtype uint8, values in {0, 1}
    memes: np.ndarray  # shape (n, N_LOCI), dtype uint8, values in {0, 1}

    @property
    def size(self) -> int:
        return self.genes.shape[0]

    def gene_fraction(self) -> np.ndarray:
        return self.genes.mean(axis=1)

    def meme_fraction(self) -> np.ndarray:
        return self.memes.mean(axis=1)

    def interactions(self) -> np.ndarray:
        """Real-valued number of interactions per individual, in [0, 200]."""
        return 100.0 * (self.gene_fraction() + self.meme_fraction())


def make_initial_population(n: int) -> Population:
    """Genes and memes both start at all-zero; both then depend entirely on
    mutation (and, for memes, contact-based spread) to create any variation
    to select on."""
    zeros = np.zeros((n, N_LOCI), dtype=np.uint8)
    return Population(genes=zeros.copy(), memes=zeros.copy())


def fitness(interactions: np.ndarray, optimum: float = OPTIMUM, width: float = 25.0) -> np.ndarray:
    """Gaussian stabilizing-selection fitness peaked at `optimum` interactions."""
    return np.exp(-((interactions - optimum) ** 2) / (2.0 * width**2))


def genetic_step(
    pop: Population,
    rng: np.random.Generator,
    optimum: float = OPTIMUM,
    width: float = 25.0,
    mutation_rate: float = 0.0005,
) -> Population:
    """One generation of Wright-Fisher selection + mutation on genes.

    Parents are resampled with replacement, weighted by fitness computed
    from each individual's current (gene + meme driven) interaction count.
    Offspring inherit the parent's genes (with per-locus mutation) and the
    parent's current memes unchanged (a proxy for vertical/upbringing
    transmission of culture, distinct from the horizontal meme-catching in
    `memetic_step`).
    """
    n = pop.size
    w = fitness(pop.interactions(), optimum=optimum, width=width)
    total = w.sum()
    probs = w / total if total > 0 else np.full(n, 1.0 / n)
    parents = rng.choice(n, size=n, p=probs, replace=True)

    new_genes = pop.genes[parents].copy()
    flips = rng.random(size=new_genes.shape) < mutation_rate
    new_genes[flips] ^= 1

    new_memes = pop.memes[parents].copy()
    return Population(genes=new_genes, memes=new_memes)


def memetic_step(
    pop: Population, rng: np.random.Generator, meme_mutation_rate: float = 0.001
) -> Population:
    """One round of meme mutation plus contact-based horizontal transmission.

    First, each meme bit independently flips with a tiny probability
    (`meme_mutation_rate`) — since memes start at all-zero, this is the only
    source of novel pro-interaction memes; contact-based spread (below) is
    what then lets a rare useful flip take over.

    Then, each individual i is given `round(interactions_i)` interaction
    "slots" (computed from the post-mutation state). Slots are shuffled and
    paired up to form the interaction meetings for this round (a
    configuration-model random matching), so individuals with more
    interactions take part in more meetings. In each meeting, both
    participants catch one meme from their partner: two independent random
    loci are drawn (one per direction), not a single shared locus, so this
    is not a swap — each side makes its own random selection of which meme
    to catch.
    """
    memes = pop.memes.copy()
    flips = rng.random(size=memes.shape) < meme_mutation_rate
    memes[flips] ^= 1

    n = pop.size
    interactions = 100.0 * (pop.gene_fraction() + memes.mean(axis=1))
    counts = np.clip(np.round(interactions).astype(int), 0, MAX_INTERACTIONS)
    stubs = np.repeat(np.arange(n), counts)
    rng.shuffle(stubs)
    if stubs.size < 2:
        return Population(genes=pop.genes.copy(), memes=memes)
    if stubs.size % 2 == 1:
        stubs = stubs[:-1]
    left = stubs[0::2]
    right = stubs[1::2]

    snapshot = memes
    new_memes = memes.copy()

    loci_for_left = rng.integers(0, N_LOCI, size=left.shape)
    loci_for_right = rng.integers(0, N_LOCI, size=right.shape)

    new_memes[left, loci_for_left] = snapshot[right, loci_for_left]
    new_memes[right, loci_for_right] = snapshot[left, loci_for_right]

    return Population(genes=pop.genes.copy(), memes=new_memes)

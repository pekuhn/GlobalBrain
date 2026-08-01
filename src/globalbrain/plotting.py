"""Renders the four-panel comparison figure."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .experiment import Trace
from .model import OPTIMUM

INK_PRIMARY = "#0b0b0b"
INK_MUTED = "#898781"
GRID_COLOR = "#e1e0d9"
DEFAULT_SURFACE = "#fcfcfb"


def _style_axes(ax, surface: str) -> None:
    ax.set_facecolor(surface)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK_MUTED)
    ax.spines["bottom"].set_color(INK_MUTED)
    ax.grid(axis="y", color=GRID_COLOR, linewidth=1, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK_MUTED, labelsize=9)
    ax.yaxis.label.set_color(INK_MUTED)
    ax.xaxis.label.set_color(INK_MUTED)
    ax.title.set_color(INK_PRIMARY)


def make_figure(
    bio_only: Trace, bio_and_memetic: Trace, out_path: str, surface: str = DEFAULT_SURFACE
) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(11, 8), sharex=True)
    fig.patch.set_facecolor(surface)

    rows = [
        ("Biological evolution only (memes off)", bio_only, False),
        ("Biological + cultural evolution", bio_and_memetic, True),
    ]

    for row, (title, trace, show_culture) in enumerate(rows):
        turns = range(len(trace.mean_interactions))

        ax_left = axes[row, 0]
        _style_axes(ax_left, surface)
        ax_left.plot(turns, trace.mean_interactions, color=INK_PRIMARY, linestyle=":", linewidth=2)
        ax_left.axhline(
            OPTIMUM,
            color=INK_MUTED,
            linestyle="--",
            linewidth=1,
            label=f"biological optimum ({OPTIMUM:.0f})",
        )
        ax_left.set_ylabel("mean interactions / turn")
        ax_left.set_title(f"{title}\nmean interactions", fontsize=11, pad=10)
        ax_left.legend(loc="best", fontsize=8, frameon=False, labelcolor=INK_PRIMARY)

        ax_right = axes[row, 1]
        _style_axes(ax_right, surface)
        ax_right.plot(
            turns,
            trace.gene_component,
            color=INK_PRIMARY,
            linestyle=":",
            linewidth=2,
            label="genetically preferred",
        )
        if show_culture:
            ax_right.plot(
                turns,
                trace.meme_component,
                color=INK_PRIMARY,
                linestyle="-",
                linewidth=2,
                label="culturally preferred",
            )
        ax_right.set_ylabel("preferred interactions / turn")
        ax_right.set_title(
            f"{title}\ngenetic{' vs. cultural' if show_culture else ''} preference", fontsize=11, pad=10
        )
        ax_right.legend(loc="best", fontsize=8, frameon=False, labelcolor=INK_PRIMARY)

    for ax in axes[-1, :]:
        ax.set_xlabel("turn")

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, facecolor=surface)
    plt.close(fig)

from .experiment import run_both_conditions
from .plotting import make_figure

OUTPUT_PATH = "evolution.png"
OUTPUT_PATH_BG = "evolution_bg.png"

# Sampled directly from the solid color in color.png.png, used as the chart
# surface for the themed variant.
BG_COLOR = "#fef2f2"


def main() -> None:
    bio_only, bio_and_memetic = run_both_conditions()
    make_figure(bio_only, bio_and_memetic, OUTPUT_PATH)
    make_figure(bio_only, bio_and_memetic, OUTPUT_PATH_BG, surface=BG_COLOR)
    print(f"Wrote {OUTPUT_PATH} and {OUTPUT_PATH_BG}")

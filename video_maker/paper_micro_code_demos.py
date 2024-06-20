import common, os
from alive_progress import alive_bar

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)

names = ["code_capacity", "circuit_level", "phenomenological"]

for name in names:
    filename = f"micro_paper_{name}_demo"
    URL = f"http://localhost:8095/index.html?animation={filename}&scale={SCALE}"
    with common.ScreenshotMaker(
        URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False
    ) as maker:
        maker.make_screenshot(0, f"{filename}.png")

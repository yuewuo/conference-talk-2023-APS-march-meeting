import common, os
from alive_progress import alive_bar

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)

URL = f"http://localhost:8095/index.html?animation=example_mle&scale={SCALE}"
with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    maker.make_screenshot(0, f"example_mle.png")

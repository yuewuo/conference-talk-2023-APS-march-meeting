import common, os
from alive_progress import alive_bar

WIDTH = int(335)
HEIGHT = WIDTH

URL = f"http://localhost:8095/index.html?animation=legend_single_x_error&scale=2"
with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False, crop_image=True) as maker:
    maker.make_screenshot(0, f"legend_single_x_error.png")

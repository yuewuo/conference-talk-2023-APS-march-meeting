import common, os
from alive_progress import alive_bar

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)

URL = f"http://localhost:8095/index.html?animation=paper_micro_blossom_fusion_demo&scale={SCALE}"
for i in range(11):
    with common.ScreenshotMaker(
        URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False
    ) as maker:
        maker.make_screenshot(i, f"paper_micro_blossom_fusion_demo_{i}.png")

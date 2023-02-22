import common, os
from alive_progress import alive_bar

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)

URL = f"http://localhost:8095/index.html?animation=surface_code&scale={SCALE}"
with common.ScreenshotMaker(URL, WIDTH, HEIGHT) as maker:
    maker.make_screenshot(0, f"surface_code.png")


URL = f"http://localhost:8095/index.html?animation=surface_code&scale={SCALE}&hide_x"
with common.ScreenshotMaker(URL, WIDTH, HEIGHT) as maker:
    maker.make_screenshot(0, f"surface_code_only_z.png")




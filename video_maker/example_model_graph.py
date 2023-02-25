import common, os, time
from alive_progress import alive_bar

SCALE = 2
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)

URL = f"http://localhost:8095/index.html?animation=example_model_graph&scale={SCALE}"
with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    time.sleep(1)
    maker.make_screenshot(0, f"example_model_graph.png")

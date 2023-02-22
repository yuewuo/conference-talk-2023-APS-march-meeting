import common, os, time
from alive_progress import alive_bar

FOLDER = "screenshots_decoding_graph"
common.create_folder(FOLDER)

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)
URL = f"http://localhost:8095/index.html?animation=decoding_graph&scale={SCALE}"
FRAME_RATE = 60
# FRAME_RATE = 5  # for debugging
DURATION = 20

USE_EXISTING_IMAGES = False
if 'USE_EXISTING_IMAGES' in os.environ and os.environ["USE_EXISTING_IMAGES"] != "":
    USE_EXISTING_IMAGES = True

with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    count = DURATION * FRAME_RATE + 1
    time.sleep(3)  # loading three.js
    with alive_bar(count) as bar:
        for frame in range(count):
            maker.make_screenshot(frame / FRAME_RATE, f"{FOLDER}/{frame}.png"
                , use_existing_images=USE_EXISTING_IMAGES)
            bar()
    maker.make_video(FRAME_RATE, "decoding_graph.mp4")

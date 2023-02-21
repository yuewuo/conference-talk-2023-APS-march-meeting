import common, os
from alive_progress import alive_bar

FOLDER = "screenshots_errors_causing_defect"
common.create_folder(FOLDER)

SCALE = 2 / common.device_pixel_ratio
WIDTH = int(1000 * SCALE)
HEIGHT = int(1000 * SCALE)
URL = f"http://localhost:8095/index.html?animation=errors_causing_defect&scale={SCALE}"
FRAME_RATE = 60
# FRAME_RATE = 5  # for debugging
DURATION = 20

USE_EXISTING_IMAGES = False
if 'USE_EXISTING_IMAGES' in os.environ and os.environ["USE_EXISTING_IMAGES"] != "":
    USE_EXISTING_IMAGES = True

with common.ScreenshotMaker(URL, WIDTH, HEIGHT) as maker:
    count = DURATION * FRAME_RATE + 1
    with alive_bar(count) as bar:
        for frame in range(count):
            maker.make_screenshot(frame / FRAME_RATE, f"{FOLDER}/{frame}.png"
                , use_existing_images=USE_EXISTING_IMAGES)
            bar()
    maker.make_video(FRAME_RATE, "errors_causing_defect.mp4")

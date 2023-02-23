import common, os, time
from alive_progress import alive_bar

FOLDER = "screenshots_example_both_grow_single"
common.create_folder(FOLDER)

SCALE = 1 / common.device_pixel_ratio
WIDTH = int(4500 * SCALE)
HEIGHT = int(2000 * SCALE)
URL = f"http://localhost:8095/index.html?animation=example_both_grow_single&scale={SCALE}"
FRAME_RATE = 60
# FRAME_RATE = 5  # for debugging
DURATION = 2.5

USE_EXISTING_IMAGES = False
if 'USE_EXISTING_IMAGES' in os.environ and os.environ["USE_EXISTING_IMAGES"] != "":
    USE_EXISTING_IMAGES = True

"""
need a large-enough monitor (at least 4500 * 2000) to take the video, because headless mode doesn't work somehow
On macOS, you can use https://github.com/waydabber/BetterDisplay to add dummy display and mirror it to your main display
"""

with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    count = int(DURATION * FRAME_RATE + 1)
    time.sleep(5)  # loading three.js
    with alive_bar(count) as bar:
        for frame in range(count):
            maker.make_screenshot(frame / FRAME_RATE, f"{FOLDER}/{frame}.png"
                , use_existing_images=USE_EXISTING_IMAGES)
            bar()
    maker.make_video(FRAME_RATE, "example_both_grow_single.mp4")

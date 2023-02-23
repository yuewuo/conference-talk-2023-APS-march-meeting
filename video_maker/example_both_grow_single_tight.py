import common, os, time
from alive_progress import alive_bar

WIDTH = 4500
HEIGHT = 2000
URL = f"http://localhost:8095/index.html?animation=example_both_grow_single_tight&scale=2"

"""
need a large-enough monitor (at least 4500 * 2000) to take the video, because headless mode doesn't work somehow
On macOS, you can use https://github.com/waydabber/BetterDisplay to add dummy display and mirror it to your main display
"""

with common.ScreenshotMaker(URL, WIDTH, HEIGHT, sleep_interval=0.5, headless=False) as maker:
    time.sleep(5)  # loading three.js
    maker.make_screenshot(0, f"example_both_grow_single_tight.png")

# scripts/shoot_final.py
# Final pass: README hero shot (docs/screenshots/ui_main.png), full-page
# desktop verification, and mobile hero with the zoomed plate.
import os
import sys
from playwright.sync_api import sync_playwright

URL = "http://localhost:8502"
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TMP = sys.argv[1] if len(sys.argv) > 1 else "shots"

with sync_playwright() as p:
    browser = p.chromium.launch()
    pg = browser.new_page(viewport={"width": 1440, "height": 1000},
                          color_scheme="light", device_scale_factor=1.5)
    pg.goto(URL, wait_until="networkidle", timeout=60000)
    pg.wait_for_selector(".cx-title", timeout=60000)
    pg.wait_for_timeout(2000)

    chip = pg.locator('[class*="st-key-chip1"] button')  # VAR overturn question
    chip.scroll_into_view_if_needed()
    chip.click()
    pg.wait_for_selector(".rec", timeout=150000)
    pg.wait_for_timeout(2500)

    rec = pg.locator(".rec")
    rec.scroll_into_view_if_needed()
    pg.wait_for_timeout(800)
    rec.screenshot(path=os.path.join(REPO, "docs", "screenshots", "ui_main.png"))
    print("README ui_main.png written")

    pg.screenshot(path=f"{TMP}_final_full.png", full_page=True)
    print("desktop full-page done")

    pm = browser.new_page(viewport={"width": 390, "height": 844},
                          color_scheme="light", device_scale_factor=2)
    pm.goto(URL, wait_until="networkidle", timeout=60000)
    pm.wait_for_selector(".cx-title", timeout=60000)
    pm.wait_for_timeout(1500)
    pm.screenshot(path=f"{TMP}_final_mob.png")
    print("mobile hero done")
    browser.close()

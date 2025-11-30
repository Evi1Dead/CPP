from __future__ import annotations

from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

from features.support.config import BASE_URLS, DEFAULT_PAGE, SELENIUM

ARTIFACT_DIR = (Path(__file__).resolve().parents[1] / ".." / "artifacts").resolve()
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def _build_options() -> Options:
    options = Options()
    if SELENIUM.get("headless", True):
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = "/usr/bin/chromium"
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    return options


def before_all(context):
    context.base_urls = BASE_URLS
    context.default_page_key = DEFAULT_PAGE
    context.artifact_dir = ARTIFACT_DIR


def before_scenario(context, scenario):
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    service = Service(driver_path)
    options = _build_options()
    context.browser = webdriver.Chrome(service=service, options=options)
    context.browser.set_page_load_timeout(SELENIUM.get("page_load", 30))
    context.browser.implicitly_wait(SELENIUM.get("implicit_wait", 5))
    context.storage = {}


def after_scenario(context, scenario):
    if scenario.status == "failed" and getattr(context, "browser", None):
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        safe_name = scenario.name.lower().replace(" ", "_")
        screenshot_path = context.artifact_dir / f"{safe_name}_{timestamp}.png"
        context.browser.save_screenshot(str(screenshot_path))
        if hasattr(context, "embed"):
            with open(screenshot_path, "rb") as image_file:
                context.embed("image/png", image_file.read(), "failure screenshot")
    if getattr(context, "browser", None):
        context.browser.quit()

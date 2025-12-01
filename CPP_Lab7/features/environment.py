from __future__ import annotations

from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager, ChromeType

from features.support.artifacts import (
    build_results_snapshot,
    ensure_artifacts_list,
    register_failure_screenshot,
    reset_artifacts,
)
from features.support.config import BASE_URL, SELENIUM
from features.support.reporting import generate_variant_report

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = PROJECT_ROOT / "artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
HEADLESS_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
)


def _apply_stealth_tweaks(driver: WebDriver) -> None:
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": (
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
                "window.chrome = { runtime: {} };"
                "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});"
                "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});"
            )
        },
    )


def _build_local_driver() -> WebDriver:
    options = ChromeOptions()
    if SELENIUM.get("headless", True):
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--user-agent={HEADLESS_USER_AGENT}")
    service = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.CHROMIUM
        ).install()
    )
    driver = webdriver.Chrome(service=service, options=options)
    _apply_stealth_tweaks(driver)
    return driver


def before_all(context) -> None:
    context.base_url = BASE_URL
    context.artifact_dir = ARTIFACT_DIR
    context.run_results = []
    ensure_artifacts_list(context)
    reset_artifacts(context)


def before_scenario(context, scenario) -> None:
    ensure_artifacts_list(context)
    reset_artifacts(context)

    context.browser = _build_local_driver()
    context.browser.set_page_load_timeout(SELENIUM.get("page_load_timeout", 30))
    context.browser.implicitly_wait(SELENIUM.get("implicit_wait", 5))
    context.storage = {}


def after_scenario(context, scenario) -> None:
    driver = getattr(context, "browser", None)
    if driver and scenario.status == "failed":
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filename = f"{scenario.name.lower().replace(' ', '_')}_{timestamp}.png"
        screenshot_path = context.artifact_dir / filename
        driver.save_screenshot(str(screenshot_path))
        register_failure_screenshot(context, "failure screenshot", screenshot_path)
        if hasattr(context, "embed"):
            with open(screenshot_path, "rb") as png:
                context.embed("image/png", png.read(), "failure screenshot")
    if driver:
        driver.quit()

    context.run_results.append(build_results_snapshot(context, scenario))
    reset_artifacts(context)


def after_all(context) -> None:
    if getattr(context, "run_results", None):
        generate_variant_report(context.run_results)

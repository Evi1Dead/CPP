from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .locators import get_locator

DEFAULT_TIMEOUT = 20
CONSENT_SELECTORS = (
    "button#L2AGLb",
    "button[aria-label='Accept all']",
    "button[aria-label='Alle accepteren']",
)
CONSENT_IFRAMES = (
    "iframe[src*='consent.google.com']",
    "iframe[name='callout']",
)


def wait_for_visibility(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    locator = get_locator(locator_key)
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_for_presence(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    locator = get_locator(locator_key)
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))


def wait_for_all(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    locator = get_locator(locator_key)
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))


def ensure_home_button_visible(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    try:
        return wait_for_visibility(driver, locator_key, timeout)
    except TimeoutException:
        search_box = wait_for_visibility(driver, "home.search_box", timeout)
        search_box.click()
        search_box.send_keys("selenium test")
        search_box.clear()
        return wait_for_visibility(driver, locator_key, timeout)


def dismiss_consent_if_needed(context):
    driver = context.browser
    iframe = None
    for selector in CONSENT_IFRAMES:
        try:
            iframe = driver.find_element(By.CSS_SELECTOR, selector)
            driver.switch_to.frame(iframe)
            break
        except NoSuchElementException:
            continue
    for selector in CONSENT_SELECTORS:
        try:
            button = driver.find_element(By.CSS_SELECTOR, selector)
            button.click()
            break
        except NoSuchElementException:
            continue
    if iframe is not None:
        driver.switch_to.default_content()

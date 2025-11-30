from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .locators import get_locator


DEFAULT_TIMEOUT = 15


def wait_for_visibility(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    locator = get_locator(locator_key)
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_for_all_visible(driver: WebDriver, locator_key: str, timeout: int = DEFAULT_TIMEOUT):
    locator = get_locator(locator_key)
    return WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located(locator))


def collect_text(elements):
    return [el.text.strip() for el in elements if el.text]


def collect_prices(elements) -> List[float]:
    prices = []
    for el in elements:
        raw = el.text.strip().replace("$", "")
        try:
            prices.append(float(raw))
        except ValueError:
            continue
    return prices


def assert_sorted(values: List[float], reverse: bool = False):
    ordered = sorted(values, reverse=reverse)
    if values != ordered:
        raise AssertionError(f"Values are not sorted correctly. Expected {ordered}, got {values}")

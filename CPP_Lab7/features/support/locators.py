from __future__ import annotations

from selenium.webdriver.common.by import By

LOCATORS = {
    "home.search_box": (By.CSS_SELECTOR, "textarea[name='q'], input[name='q']"),
    "home.search_button": (By.CSS_SELECTOR, ".FPdoLc input[name='btnK']"),
    "home.feeling_lucky": (By.CSS_SELECTOR, ".FPdoLc input[name='btnI']"),
    "home.logo": (By.CSS_SELECTOR, "img[alt='Google']"),
    "results.container": (By.ID, "search"),
    "results.organic_cards": (By.CSS_SELECTOR, "#search div.g"),
    "results.did_you_mean": (By.CSS_SELECTOR, "a[aria-label^='Did you mean'], a.spell_orig"),
    "results.no_results": (By.CSS_SELECTOR, "#topstuff .card-section, #topstuff .vOY7J"),
    "results.autocomplete_list": (By.CSS_SELECTOR, "ul[role='listbox']"),
    "results.autocomplete_items": (By.CSS_SELECTOR, "ul[role='listbox'] li span"),
    "results.titles": (By.CSS_SELECTOR, "#search h3"),
    "knowledge.calculator_result": (By.ID, "cwos"),
    "knowledge.currency_widget": (
        By.CSS_SELECTOR,
        "div[data-exchange-rate], div.knowledge-currency__updatable-data-column",
    ),
}


def get_locator(key: str):
    if key not in LOCATORS:
        available = "\n - ".join(sorted(LOCATORS))
        raise KeyError(f"Unknown locator '{key}'. Known keys:\n - {available}")
    return LOCATORS[key]

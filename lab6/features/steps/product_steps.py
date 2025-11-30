from __future__ import annotations

from behave import then, when
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from features.support.helpers import wait_for_all_visible, wait_for_visibility


@then('every product card should expose image title and price')
def step_product_card_content(context):
    cards = wait_for_all_visible(context.browser, "product.cards")
    issues = []
    for idx, card in enumerate(cards, start=1):
        try:
            card.find_element(By.CSS_SELECTOR, ".men-thumb-item .pro-image-front")
            card.find_element(By.CSS_SELECTOR, ".item-info-product h4 a")
            price = card.find_element(By.CSS_SELECTOR, ".item-info-product .item_price").text.strip()
            if not price.startswith("$"):
                issues.append(f"Card {idx} price missing currency symbol")
        except Exception as exc:  # pragma: no cover - Selenium raises detailed errors
            issues.append(f"Card {idx} missing field: {exc}")
    if issues:
        raise AssertionError("\n".join(issues))


@when('I open the details page for the first product')
def step_open_first_pdp(context):
    first_link = wait_for_all_visible(context.browser, "product.card.title")[0]
    context.storage['selected_product'] = first_link.text.strip()
    first_link.click()
    WebDriverWait(context.browser, 10).until(EC.url_contains("/single"))


@then('the PDP should load without rendering errors')
def step_verify_pdp(context):
    wait_for_visibility(context.browser, "pdp.heading")
    wait_for_visibility(context.browser, "pdp.price")
    if not context.browser.current_url.endswith("/single"):
        raise AssertionError("Expected to be on the PDP /single endpoint")

from __future__ import annotations

import time

from behave import when, then
from selenium.webdriver.support.ui import Select

from features.support.helpers import (
    assert_sorted,
    collect_prices,
    wait_for_all_visible,
    wait_for_visibility,
)


@when('I capture the current product prices')
def step_capture_prices(context):
    price_elements = wait_for_all_visible(context.browser, "product.card.price")
    context.storage['prices'] = collect_prices(price_elements)


@when('I sort products by option "{label}"')
def step_sort_products(context, label):
    dropdown = wait_for_visibility(context.browser, "sorting.dropdown")
    Select(dropdown).select_by_visible_text(label)
    time.sleep(1.5)  # allow the page script to reorder (low impact demo site)
    price_elements = wait_for_all_visible(context.browser, "product.card.price")
    context.storage['prices'] = collect_prices(price_elements)


@then('the captured prices should be sorted from high to low')
def step_validate_high_to_low(context):
    assert_sorted(context.storage.get('prices', []), reverse=True)


@then('the captured prices should be sorted from low to high')
def step_validate_low_to_high(context):
    assert_sorted(context.storage.get('prices', []), reverse=False)

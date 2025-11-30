from __future__ import annotations

import time

from behave import given, when, then
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from features.support.locators import get_locator
from features.support.helpers import wait_for_visibility


def _open_mini_cart(context):
    cart_button = wait_for_visibility(context.browser, "header.cart_button")
    cart_button.click()
    locator = get_locator("cart.mini")
    try:
        WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        raise AssertionError("Mini cart container did not appear; PayPal widget failed to render")


def _ensure_cart_item(context):
    add_buttons = context.browser.find_elements(*get_locator("product.card.add_to_cart"))
    if not add_buttons:
        raise AssertionError("No Add to cart buttons located on catalog")
    add_buttons[0].click()
    time.sleep(1)
    _open_mini_cart(context)
    context.storage['cart_seeded'] = True


def _first_qty_input(context):
    locator = get_locator("cart.qty_inputs")
    try:
        return WebDriverWait(context.browser, 5).until(EC.visibility_of_element_located(locator))
    except TimeoutException:
        raise AssertionError("Mini cart does not expose any quantity inputs (known bug from Lab 3)")


@when('I add the first product to the cart from the catalog')
def step_add_first_product(context):
    _ensure_cart_item(context)


@then('the mini cart should display the product with quantity "{qty}"')
def step_validate_cart_qty(context, qty):
    qty_input = _first_qty_input(context)
    value = qty_input.get_attribute("value")
    if value != qty:
        raise AssertionError(f"Expected qty {qty}, got {value}")


@given('the mini cart already contains an item')
def step_cart_contains_item(context):
    if not context.storage.get('cart_seeded'):
        _ensure_cart_item(context)
    else:
        _open_mini_cart(context)


@when('I update the mini cart quantity to "{qty}"')
def step_update_qty(context, qty):
    qty_input = _first_qty_input(context)
    qty_input.clear()
    qty_input.send_keys(qty)
    qty_input.send_keys(Keys.ENTER)
    context.storage['cart_qty'] = qty


@when('I refresh the mini cart view')
def step_refresh_mini_cart(context):
    context.browser.refresh()
    wait_for_visibility(context.browser, "product.grid")
    _open_mini_cart(context)


@then('the mini cart quantity should persist as "{qty}"')
def step_qty_persists(context, qty):
    actual = _first_qty_input(context).get_attribute("value")
    if actual != qty:
        raise AssertionError(f"Qty did not persist. Expected {qty}, got {actual}")


@when('I attempt to set the mini cart quantity to "{qty}"')
def step_set_invalid_qty(context, qty):
    step_update_qty(context, qty)


@then('a validation error or warning should be displayed')
def step_validate_error(context):
    locator = get_locator("cart.error")
    errors = context.browser.find_elements(*locator)
    if not errors:
        raise AssertionError("Expected an error/warning banner for invalid quantity")


@then('the checkout button should remain disabled until values are valid')
def step_checkout_disabled(context):
    checkout = wait_for_visibility(context.browser, "cart.checkout")
    if checkout.is_enabled():
        raise AssertionError("Checkout button should be disabled while quantity is invalid")

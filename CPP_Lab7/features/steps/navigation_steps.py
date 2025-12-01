from __future__ import annotations

from behave import given, then

from features.support.helpers import (
    dismiss_consent_if_needed,
    ensure_home_button_visible,
    wait_for_visibility,
)

HOME_BUTTON_KEYS = {"home.search_button", "home.feeling_lucky"}


@given("I open the Google home page")
def step_open_home(context):
    context.browser.get(context.base_url)
    dismiss_consent_if_needed(context)


@then('the page title should contain "{text}"')
def step_check_title(context, text):
    if text.lower() not in context.browser.title.lower():
        raise AssertionError(f"Expected '{text}' in title, got '{context.browser.title}'")


@then("the following elements should be visible")
def step_visible_elements(context):
    for row in context.table:
        locator_key = row["locator_key"]
        if locator_key in HOME_BUTTON_KEYS:
            ensure_home_button_visible(context.browser, locator_key)
        else:
            wait_for_visibility(context.browser, locator_key)


@then("the Google logo should be displayed")
def step_logo_visible(context):
    logo = wait_for_visibility(context.browser, "home.logo")
    if not logo.is_displayed():
        raise AssertionError("Google logo is not displayed")

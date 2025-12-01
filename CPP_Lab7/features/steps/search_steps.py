from __future__ import annotations

from behave import then, when
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from features.support.artifacts import dump_debug_artifacts
from features.support.helpers import (
    dismiss_consent_if_needed,
    wait_for_presence,
    wait_for_visibility,
)


@when('I search for "{query}"')
def step_perform_search(context, query):
    dismiss_consent_if_needed(context)
    box = wait_for_visibility(context.browser, "home.search_box")
    box.clear()
    box.send_keys(query)
    box.send_keys(Keys.ENTER)
    try:
        wait_for_presence(context.browser, "results.container")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "results_timeout")
        raise AssertionError(
            f"Timed out waiting for results when searching '{query}'."
        ) from exc


@then('at least {minimum:d} organic results should be shown')
def step_min_results(context, minimum):
    try:
        wait_for_presence(context.browser, "results.organic_cards")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "organic_timeout")
        raise AssertionError("Google results container never rendered.") from exc
    cards = context.browser.find_elements(By.CSS_SELECTOR, "#search div.g")
    visible_cards = [card for card in cards if card.is_displayed()]
    actual = len(visible_cards)
    if actual < minimum:
        dump_debug_artifacts(context, "insufficient_results")
        raise AssertionError(f"Expected >= {minimum} results, got {actual}")


@then('no more than {maximum:d} organic results should be shown')
def step_max_results(context, maximum):
    cards = context.browser.find_elements(By.CSS_SELECTOR, "#search div.g")
    visible_cards = [card for card in cards if card.is_displayed()]
    actual = len(visible_cards)
    if actual > maximum:
        dump_debug_artifacts(context, "too_many_results")
        raise AssertionError(f"Expected <= {maximum} results, got {actual}")


@when("I submit an empty query")
def step_submit_empty(context):
    dismiss_consent_if_needed(context)
    box = wait_for_visibility(context.browser, "home.search_box")
    box.clear()
    box.send_keys(Keys.ENTER)


@then("I should remain on the Google home page")
def step_validate_home(context):
    current = context.browser.current_url
    if not current.startswith("https://www.google."):
        dump_debug_artifacts(context, "unexpected_redirect")
        raise AssertionError(f"Expected to stay on Google home, current URL is {current}")


@then("no results section should be visible")
def step_no_results(context):
    try:
        container = context.browser.find_element(By.ID, "search")
        if container.is_displayed():
            dump_debug_artifacts(context, "results_visible_for_empty")
            raise AssertionError("Results container should not be visible for empty search")
    except NoSuchElementException:
        return


@then('the "Did you mean" suggestion should be visible')
def step_did_you_mean(context):
    try:
        wait_for_visibility(context.browser, "results.did_you_mean")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "missing_did_you_mean")
        raise AssertionError("Expected 'Did you mean' suggestion, but none appeared.") from exc

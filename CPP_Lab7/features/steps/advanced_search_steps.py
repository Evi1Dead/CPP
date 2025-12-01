from __future__ import annotations

from behave import then, when
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from features.support.artifacts import dump_debug_artifacts
from features.support.helpers import (
    dismiss_consent_if_needed,
    wait_for_all,
    wait_for_presence,
    wait_for_visibility,
)


@then("I should see a no results message explaining there were no matches")
def step_no_results_message(context):
    try:
        banner = wait_for_visibility(context.browser, "results.no_results")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "no_results_missing")
        raise AssertionError(
            "Expected a 'did not match any documents' style message for gibberish query."
        ) from exc
    text = banner.text.lower()
    if "did not match any documents" not in text and "no results found" not in text:
        dump_debug_artifacts(context, "no_results_text_mismatch")
        raise AssertionError(f"Unexpected no-results copy: '{banner.text}'")


@when("I accept the suggested correction")
def step_accept_suggestion(context):
    try:
        suggestion = wait_for_visibility(context.browser, "results.did_you_mean")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "missing_suggestion_link")
        raise AssertionError("No 'Did you mean' link was available to click.") from exc
    context.storage["last_suggestion"] = suggestion.text.strip()
    suggestion.click()
    try:
        wait_for_presence(context.browser, "results.container")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "suggestion_no_results")
        raise AssertionError("After clicking suggestion Google never loaded results.") from exc


@then('the search box should contain "{expected}"')
def step_search_box_value(context, expected):
    box = wait_for_visibility(context.browser, "home.search_box")
    actual = box.get_attribute("value")
    if expected.lower() != (actual or "").lower():
        dump_debug_artifacts(context, "search_box_value_mismatch")
        raise AssertionError(f"Expected search box value '{expected}', got '{actual}'")


@when('I type "{text}" into the search box without submitting')
def step_type_without_submit(context, text):
    dismiss_consent_if_needed(context)
    box = wait_for_visibility(context.browser, "home.search_box")
    box.clear()
    box.send_keys(text)
    context.storage["typed_query"] = text


@then('I should see autocomplete suggestions containing "{expected}"')
def step_autocomplete_contains(context, expected):
    try:
        wait_for_visibility(context.browser, "results.autocomplete_list")
        suggestions = wait_for_all(context.browser, "results.autocomplete_items")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "autocomplete_missing")
        raise AssertionError("Autocomplete list never appeared.") from exc
    texts = [s.text.strip().lower() for s in suggestions if s.text.strip()]
    match = any(expected.lower() in text for text in texts)
    if not match:
        dump_debug_artifacts(context, "autocomplete_no_match")
        raise AssertionError(
            f"Autocomplete suggestions did not include '{expected}'. Actual: {texts}"
        )


@then('the first organic result should contain "{phrase}"')
def step_first_result_contains(context, phrase):
    titles = _load_first_result_element(context)
    first_text = titles[0].text.strip().lower()
    if phrase.lower() not in first_text:
        dump_debug_artifacts(context, "first_result_missing_phrase")
        raise AssertionError(
            f"Expected first result to contain '{phrase}', but got '{titles[0].text}'."
        )


@when('I store the first organic result title as "{key}"')
def step_store_first_result(context, key):
    titles = _load_first_result_element(context)
    context.storage[key] = titles[0].text.strip()


@then('the first organic result title should match "{key}"')
def step_compare_first_result(context, key):
    if key not in context.storage:
        raise AssertionError(f"No stored result found under key '{key}'.")
    titles = _load_first_result_element(context)
    current = titles[0].text.strip()
    baseline = context.storage[key].strip()
    if current != baseline:
        dump_debug_artifacts(context, "case_sensitivity_mismatch")
        raise AssertionError(
            f"Expected first result '{baseline}' to match '{current}' ignoring case differences."
        )


@then('the calculator result should display "{value}"')
def step_calculator_output(context, value):
    try:
        result = wait_for_visibility(context.browser, "knowledge.calculator_result")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "calculator_missing")
        raise AssertionError("Calculator widget did not render for math query.") from exc
    actual = result.text.strip()
    if actual != value:
        dump_debug_artifacts(context, "calculator_value_mismatch")
        raise AssertionError(f"Expected calculator result '{value}', got '{actual}'")


@then("the currency converter widget should be visible")
def step_currency_widget(context):
    try:
        widget = wait_for_visibility(context.browser, "knowledge.currency_widget")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "currency_widget_missing")
        raise AssertionError("Currency converter widget did not appear.") from exc
    if not widget.is_displayed():
        dump_debug_artifacts(context, "currency_widget_hidden")
        raise AssertionError("Currency converter widget exists but is hidden.")


def _load_first_result_element(context):
    try:
        titles = wait_for_all(context.browser, "results.titles")
    except TimeoutException as exc:
        dump_debug_artifacts(context, "result_titles_missing")
        raise AssertionError("Search results never rendered titles to inspect.") from exc
    visible = [title for title in titles if title.is_displayed()]
    if not visible:
        dump_debug_artifacts(context, "result_titles_not_visible")
        raise AssertionError("No visible result titles found.")
    return visible

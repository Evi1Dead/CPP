from __future__ import annotations

from behave import given, then
from selenium.webdriver.common.by import By
import requests

from features.support.helpers import wait_for_all_visible, wait_for_visibility


@given('I open the "{page_key}" page')
def step_open_page(context, page_key):
    target = context.base_urls.get(page_key)
    if not target:
        raise ValueError(f"Unknown page key '{page_key}'. Available: {', '.join(context.base_urls.keys())}")
    context.browser.get(target)


@then('the page title should contain "{text}"')
def step_check_title(context, text):
    title = context.browser.title
    if text.lower() not in title.lower():
        raise AssertionError(f"Expected '{text}' in title, got '{title}'")


@then('no javascript errors should be present in the console')
def step_no_js_errors(context):
    try:
        logs = context.browser.get_log('browser')
    except Exception as exc:  # pragma: no cover - depends on driver support
        raise AssertionError(f"Unable to collect browser logs: {exc}") from exc
    severe = [entry for entry in logs if entry.get('level') == 'SEVERE']
    if severe:
        messages = "\n".join(f"[{e['level']}] {e['message']}" for e in severe)
        raise AssertionError(f"Found JavaScript errors:\n{messages}")


@then('the product grid should contain at least {expected:d} cards')
def step_min_cards(context, expected):
    cards = wait_for_all_visible(context.browser, "product.cards")
    if len(cards) < expected:
        raise AssertionError(f"Expected >= {expected} cards, got {len(cards)}")


@then('the following elements should be visible')
def step_elements_visible(context):
    for row in context.table:
        locator_key = row['locator_key']
        wait_for_visibility(context.browser, locator_key)


@then('each header link should be reachable')
def step_header_links_reachable(context):
    links = context.browser.find_elements(By.CSS_SELECTOR, ".menu__list a")
    unreachable = []
    for link in links:
        href = link.get_attribute('href')
        if not href:
            continue
        try:
            response = requests.head(href, allow_redirects=True, timeout=10)
        except requests.RequestException as exc:  # pragma: no cover
            unreachable.append((href, str(exc)))
            continue
        if response.status_code >= 400:
            unreachable.append((href, f"HTTP {response.status_code}"))
    if unreachable:
        details = "\n".join(f"{url} -> {err}" for url, err in unreachable)
        raise AssertionError(f"Broken navigation links detected:\n{details}")

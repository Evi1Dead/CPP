from __future__ import annotations

from selenium.webdriver.common.by import By

LOCATORS = {
    # Header
    "header.top_links": (By.CSS_SELECTOR, ".header ul li"),
    "header.search": (By.CSS_SELECTOR, ".header-middle form"),
    "header.logo": (By.CSS_SELECTOR, ".logo_agile h1 a"),
    "header.nav": (By.CSS_SELECTOR, ".menu__list"),
    "header.cart_button": (By.CSS_SELECTOR, "button.w3view-cart"),
    # Sorting & filters
    "sorting.dropdown": (By.ID, "country1"),
    "sorting.active_label": (By.CSS_SELECTOR, ".sorting h6"),
    # Product content
    "product.grid": (By.CSS_SELECTOR, ".single-pro"),
    "product.cards": (By.CSS_SELECTOR, ".single-pro .product-men"),
    "product.card.title": (By.CSS_SELECTOR, ".item-info-product h4 a"),
    "product.card.price": (By.CSS_SELECTOR, ".item-info-product .item_price"),
    "product.card.image.front": (By.CSS_SELECTOR, ".men-thumb-item .pro-image-front"),
    "product.card.image.back": (By.CSS_SELECTOR, ".men-thumb-item .pro-image-back"),
    "product.card.quick_view": (By.CSS_SELECTOR, "a.link-product-add-cart"),
    "product.card.add_to_cart": (By.CSS_SELECTOR, "form[action='#'] input[type='submit']"),
    # PDP selectors
    "pdp.heading": (By.CSS_SELECTOR, ".single-right-left.simpleCart_shelfItem h3"),
    "pdp.price": (By.CSS_SELECTOR, ".single-right-left.simpleCart_shelfItem .item_price"),
    # Cart & overlays (PayPal mini cart)
    "cart.mini": (By.ID, "PPMiniCart"),
    "cart.items": (By.CSS_SELECTOR, "#PPMiniCart form"),
    "cart.total": (By.CSS_SELECTOR, "#PPMiniCart .ppmini-total"),
    "cart.checkout": (By.CSS_SELECTOR, "#PPMiniCart .ppmini-checkout a"),
    "cart.qty_inputs": (By.CSS_SELECTOR, "#PPMiniCart input[name='quantity']"),
    # Toasts & errors
    "cart.error": (By.CSS_SELECTOR, ".error, .alert, .message"),
}


def get_locator(key: str):
    try:
        return LOCATORS[key]
    except KeyError as exc:
        known = "\n - ".join(sorted(LOCATORS.keys()))
        raise KeyError(f"Unknown locator '{key}'. Known keys:\n - {known}") from exc

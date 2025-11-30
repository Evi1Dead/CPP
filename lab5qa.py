from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")  # decomenteaza daca vrei fara UI
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def try_accept_cookies(driver):
    """
    Incearca sa accepte bannerul de cookies Amazon (UE).
    Conform variantei din scriptul tau mare: id=sp-cc-accept etc.
    """
    try:
        short_wait = WebDriverWait(driver, 3)

        # 1) Butonul clasic de la Amazon: id="sp-cc-accept"
        if len(driver.find_elements(By.ID, "sp-cc-accept")) > 0:
            btn = short_wait.until(EC.element_to_be_clickable((By.ID, "sp-cc-accept")))
            btn.click()
            return

        # 2) Alte variante generice cu "Accept" in text
        candidates = [
            (By.XPATH, '//input[@name="accept"]'),
            (By.XPATH, '//button[contains(., "Accept")]'),
        ]
        for by, sel in candidates:
            if len(driver.find_elements(by, sel)) > 0:
                btn = short_wait.until(EC.element_to_be_clickable((by, sel)))
                btn.click()
                return

    except Exception:
        # Daca nu exista banner sau nu poate fi apasat, ignoram
        pass


def test_amazon_header_displayed_after_search(driver):
    driver.get("https://www.amazon.com/")

    try_accept_cookies(driver)

    wait = WebDriverWait(driver, 10)

    # Câmp de cautare Amazon: id="twotabsearchtextbox"
    search_input = wait.until(
        EC.visibility_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_input.clear()
    search_input.send_keys("computer")

    # Buton de cautare: id="nav-search-submit-button"
    search_button = driver.find_element(By.ID, "nav-search-submit-button")
    search_button.click()

    # Verificam ca header-ul Amazon e vizibil pe pagina de rezultate
    # in scriptul tau mare sunt folosite: "navbar", "nav-belt", "nav-logo-sprites", "nav-logo"
    header_locators = [
        (By.ID, "navbar"),
        (By.ID, "nav-belt"),
        (By.ID, "nav-logo-sprites"),
        (By.ID, "nav-logo"),
    ]

    header = None
    for by, sel in header_locators:
        try:
            header = wait.until(
                EC.visibility_of_element_located((by, sel))
            )
            if header.is_displayed():
                break
        except Exception:
            continue

    assert header is not None and header.is_displayed(), \
        "Amazon header should be visible after searching for 'computer'."

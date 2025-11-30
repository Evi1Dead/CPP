# CPP Lab 6 – Cucumber BDD Automation

This project automates the six manual scenarios from Lab 3 against the Elite Shoppy demo site using Python, Behave (Cucumber Gherkin), and Selenium WebDriver running on Google Chrome.

## Prerequisites
- Python 3.13+
- Google Chrome (stable channel)
- ChromeDriver is provisioned automatically through `webdriver-manager`.

## Setup
```bash
cd /home/kali/Documents/CPP_Lab6
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the suite
```bash
source .venv/bin/activate
behave
```

By default the tests execute in headless Chrome against `https://adoring-pasteur-3ae17d.netlify.app/mens`. Update `features/support/config.py` if you need to point to a different environment.

## Notes
- Step definitions are grouped by functionality (navigation, sorting, product content, cart flows, negative checks).
- Generic element validation and locator resolution live in `features/support/locators.py` to keep selectors reusable and relative.
- `TC-MEN-004` and `TC-MEN-006` intentionally fail to document the known bugs described in Lab 3.

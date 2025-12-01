# CPP Lab 7 – Google Search Automation (Variants 1-3)

All lab assets (code, artifacts, reports) intentionally live under `/home/kali/Documents/CPP_Lab7` to satisfy the "Documents-folder only" constraint. The suite automates Variant 1, Variant 2, **and** Variant 3 of the Lab 7 rubric using Python, Behave, Selenium, and a local headless Chromium driver.

## What the suite covers
- **Variant 1** – smoke checks for widgets, result counts, blank submission guard, and "Did you mean" visibility.
- **Variant 2** – gibberish/no-result handling, suggestion acceptance, and autocomplete suggestions.
- **Variant 3** – multilingual searches, case-insensitivity proof, calculator widget, and currency converter widget validation.
- Every step captures actionable error messages and, on failure, writes HTML + screenshot artifacts explaining *why* Google did not behave as expected.

## Prerequisites
- Python 3.13+
- Google Chrome / Chromium available on `PATH`

## Installation
```bash
cd /home/kali/Documents/CPP_Lab7
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the suite (local Chrome/Chromium)
`behave-html-formatter` exposes a formatter class, so invoke it explicitly:
```bash
cd /home/kali/Documents/CPP_Lab7
source .venv/bin/activate
behave -f pretty -f behave_html_formatter:HTMLFormatter -o reports/behave-report.html
```
The console shows the "pretty" formatter while the HTML report (with embedded failure screenshots from `artifacts/`) lands at `reports/behave-report.html`.

## Structure highlights
- `features/google_search.feature` – Variant 1-3 scenarios, organized with tags.
- `features/steps/navigation_steps.py` – Background navigation and widget assertions.
- `features/steps/search_steps.py` – Shared search execution + generic result assertions.
- `features/steps/advanced_search_steps.py` – Variant 2 & 3-specific logic (autocomplete, calculator, converter, case comparison).
- `features/support/locators.py` – Centralized selectors.
- `features/support/helpers.py` – Wait utilities, consent modal handling, artifact capture plumbing.
- `features/support/artifacts.py` – Helper used by failing steps to dump HTML + screenshots for "why it failed" evidence.

## Notes
- BrowserStack hooks were intentionally removed per the latest requirement; everything runs locally.
- Attach both `reports/behave-report.html` and the `artifacts/` screenshots folder when submitting the lab for grading so failures (if any) include the captured “why it broke” context.

# Sauce Demo QA Automation

![Tests](https://github.com/vishnu1234-123/saucedemo-qa-automation/actions/workflows/tests.yml/badge.svg)

Functional and accessibility test automation for [saucedemo.com](https://www.saucedemo.com), a practice e-commerce site. The project covers a test plan, manual and automated test cases, a WCAG 2.1 AA accessibility audit, and CI on three browsers.

## What this project shows

- **Functional testing:** 43 test cases across login, products, cart and checkout, automated with Playwright (Python) and pytest using the Page Object Model.
- **Accessibility testing:** 17 WCAG checks. Automated with axe-core and custom Playwright checks, plus a manual audit with keyboard, VoiceOver, Colour Contrast Analyser and axe DevTools.
- **Defect management:** 12 bugs logged in Azure DevOps, one per root cause, each linked to the affected pages and the test that proves it.
- **CI:** GitHub Actions runs the suite on Chromium, Firefox and WebKit on every push, pull request and nightly.
- **Traceability:** a matrix linking test cases, WCAG criteria, pages and bugs (`docs/traceability-matrix.xlsx`).

## Findings in brief

The site passes automated axe checks for WCAG A and AA, but a manual audit found accessibility barriers that axe, WAVE and Lighthouse did not report. Examples: no visible focus indicator, a cart icon that can't be reached with the keyboard, a menu button that doesn't expose its state, page titles that are the same on every page, and focus that leaves the open menu. An automated scan passing does not mean a site is accessible.

The full list is in `docs/traceability-matrix.xlsx` (Defects sheet).

## Project structure

```
pages/        Page objects (one class per page)
helpers/      axe-core helper
tests/        Functional tests and accessibility tests
docs/         Test plan, traceability matrix, accessibility conformance report
.github/      CI workflow
conftest.py   Shared fixtures
pytest.ini    Markers and settings
```

## Setup

Requires Python 3.13.

```
git clone https://github.com/vishnu1234-123/saucedemo-qa-automation.git
cd saucedemo-qa-automation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Running the tests

```
pytest                                  # everything, Chromium
pytest --browser firefox                # another browser
pytest -m smoke                         # smoke tests only
pytest -m a11y                          # accessibility tests only
pytest --headed                         # watch the browser
```

Markers: `smoke`, `regression`, `a11y`.

## Expected failures (xfail)

Tests for known bugs are marked as expected failures and tied to the bug ID:

```python
@pytest.mark.xfail(strict=True, raises=AssertionError, reason="ADO-20: keyboard focus leaves the open menu (2.4.3)")
```

- The suite stays green while a bug is open, and the test still documents the defect.
- `strict=True` means that when a bug is fixed, the test "unexpectedly passes" and the run fails. That is the signal to remove the marker and close the bug.
- `raises=AssertionError` stops a timeout or setup error from hiding as an expected failure.

To see the failures with screenshots and traces, ignore the markers:

```
pytest -m a11y --runxfail --screenshot on --tracing on --output test-results
playwright show-trace test-results/<folder>/trace.zip
```

## Continuous integration

The workflow in `.github/workflows/tests.yml` runs a matrix of Chromium, Firefox and WebKit. It runs on push, pull request and every night at 06:00 UTC. Traces from failed runs are uploaded as artifacts.

Note: the WebKit job uses the Playwright WebKit build on Linux. It is not real Safari. Safari and mobile browsers are covered separately on real devices (see below).

## Environments tested

| Environment | How | Status |
|---|---|---|
| Chromium, Firefox, WebKit (Playwright) | CI and local | Done |
| macOS + Safari + VoiceOver | Manual | Done |
| Windows + NVDA (Firefox, Chrome) | Manual | Planned |
| Windows + JAWS (Chrome) | Manual | Planned |
| iPhone Safari, Android Chrome, TalkBack | BrowserStack real devices | Planned |

## Documents

- `docs/test-plan.md`: scope, approach, test cases, risks
- `docs/traceability-matrix.xlsx`: tests, WCAG criteria, pages and bugs
- `docs/acr.*`: accessibility conformance report (VPAT format) *(in progress)*

## Notes

- The target site is a public practice site and can change. Test dates are recorded in the test plan.
- Bugs are filed by hand, not created automatically from test failures.
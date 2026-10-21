# Test Plan: Sauce Demo (Swag Labs) Web Application

| | |
| --- | --- |
| **Version** | 0.1 (draft) |
| **Date** | 2026-10-21 |
| **Author** | Vishnu |
| **Application under test** | https://www.saucedemo.com (public demo shopping app) |
| **Repository** | `saucedemo-qa-automation` (this repo) |
| **Defect tracker / test management** | Azure DevOps project `A11y-QA-Capstone` |

---

## 1. Objective

Verify that the Sauce Demo shopping flow (login, product list, cart, checkout) works as expected and conforms to **WCAG 2.1 Level AA**, using a combination of manual testing, automated testing (Playwright with pytest) and accessibility testing (automated scans, keyboard, screen reader, contrast). Defects are logged in Azure DevOps with evidence, and the results feed an Accessibility Conformance Report (ACR) based on the ITI VPAT template.

This is a practice project on a public demo site. Fixing defects is out of scope; the goal is finding, documenting and reporting them.

## 2. Scope

**In scope**
- Pages: Login, Products (inventory), Cart, Checkout: Your Information, Checkout: Overview, Checkout: Complete, Product details, and the slide-in menu
- Functional testing: login, sorting, add/remove items, cart, checkout form validation, order totals, logout
- Accessibility testing against WCAG 2.1 AA on every page
- Cross-browser testing: Chromium, Firefox, WebKit (see Section 5)

**Out of scope**
- Performance, load and security testing
- API testing (covered in a separate project)
- Native mobile apps
- Fixing or retesting defects (the demo site is not ours to change)

## 3. Test approach

| Type | How | Tools |
| --- | --- | --- |
| Manual functional | Execute each manual test case, record pass or fail and evidence | Browser, Azure DevOps test case work items |
| Automated functional | Playwright (Python) with pytest, page object model, `data-test` locators | pytest-playwright, GitHub Actions |
| Accessibility, automated | Automated rule scans per page | axe DevTools, WAVE, Lighthouse, axe-core in Playwright |
| Accessibility, keyboard | Tab, Shift+Tab, Enter, Space, Esc; focus order and visibility | Chrome DevTools Console (`focusin` log) |
| Accessibility, screen reader | Reading order, names, roles, states, announcements | VoiceOver (macOS); NVDA via BrowserStack or a Windows machine |
| Accessibility, visual | Colour contrast, zoom 200% and 400% | Colour Contrast Analyser |
| Cross-browser | Same suite on several engines | Playwright locally and in CI, BrowserStack trial (Safari) |

**Accessibility method (four layers per page):** automated scan, then keyboard, then screen reader, then contrast and zoom. Automated results that carry an AI or "needs review" tag are verified manually before being logged.

**Tests are independent.** Every automated test starts from a fresh browser context, so no test depends on another.

## 4. Test items and Azure DevOps mapping

Epic: **Sauce Demo accessibility and functional testing**
Feature: **Shopping flow**

| User story (ADO) | Page | Test case prefix | Automated test file |
| --- | --- | --- | --- |
| Login | Login | `TC-LOGIN` | `tests/test_login.py` |
| Product list | Products, menu | `TC-INV` | `tests/test_inventory.py` |
| Cart | Cart | `TC-CART` | `tests/test_cart.py` |
| Checkout: your information | Checkout step one | `TC-CHKI` | `tests/test_checkout_information.py` |
| Checkout: overview | Checkout step two | `TC-CHKO` | `tests/test_checkout_overview.py` |
| Checkout: complete | Order complete | `TC-CHKC` | `tests/test_checkout_complete.py` |
| Product details (to be recreated) | Product details | `TC-PD` | not yet |

Accessibility checks use the prefix `TC-A11Y` and are run on every page (Section 11).

## 5. Test environments

| Environment | Details | Use |
| --- | --- | --- |
| Local | macOS 14.1.2 (Apple Silicon), Chrome, Python 3.13, Playwright 1.64 | Manual testing, local runs on Chromium and Firefox |
| Local, WebKit | Not available: WebKit on macOS 14 crashes on launch with this Playwright version (the WebKit build for macOS 14 is no longer supported) | Covered in CI instead |
| CI | GitHub Actions, Ubuntu runner | Chromium, Firefox and WebKit |
| Cloud | BrowserStack free trial | Safari run on a subset (smoke and accessibility); NVDA if available |
| Screen readers | VoiceOver on macOS; NVDA via BrowserStack; JAWS demo to be tried | Manual accessibility checks |

## 6. Test data

Public demo credentials displayed on the login page (not secrets).

| User | Purpose |
| --- | --- |
| `standard_user` | Main user for functional and accessibility testing |
| `locked_out_user` | Negative login |
| `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` | Persona tests; behaviour to be explored and documented before testing |
| Password for all users | Shown on the login page |

Checkout data: use dummy values only (for example first name `Test`, last name `User`, postal code `12345`).

## 7. Entry and exit criteria

**Entry**
- Test cases written and reviewed
- Environments available (local browsers, repo set up, ADO project accessible)
- Test data identified

**Exit**
- All test cases executed and results recorded
- Every failed case has a linked defect in Azure DevOps
- No Severity 1 or 2 defect left untriaged
- Automated suite passing in CI on the agreed browsers, apart from tests marked as expected failures that reference a known defect
- ACR drafted from the audit results

## 8. Severity and priority

| Severity | Meaning | Example |
| --- | --- | --- |
| 1 - Critical | A user cannot complete a core task and there is no workaround | Core flow unusable with a keyboard or screen reader |
| 2 - High | A user is blocked or seriously hindered, with difficult workarounds | Controls unreachable by keyboard; no visible focus indicator |
| 3 - Medium | A user is hindered but can complete the task | Placeholder-only labels; constant page title; missing headings |
| 4 - Low | Minor issue or inconvenience | Missing `autocomplete`; unusual tab order for a closed control |

Severity is rated by user impact and WCAG level. Final ratings follow the guidance of the mentor or team lead when it differs.

## 9. Defect management

- **Tracker:** Azure DevOps, Bug work items
- **Title format:** `[A11y][WCAG SC] description, platform` for accessibility defects; `[Func] description, platform` for functional defects
- **Required fields:** severity, steps to reproduce, expected result, actual result, element or selector, impact, environment (browser, OS, assistive technology), attachments
- **Links:** Parent link to the user story for the page; Related links to the same issue on other pages or to a duplicate bug
- **Site-wide issues** (same root cause on several pages) are logged once, with a Pages affected list, and linked Related from each page's story
- **Automated failures** are triaged first (real defect, flaky test, or test error) and logged manually; the ADO bug ID is recorded in the test's expected-failure reason

## 10. Test cases

Legend: **A** = automated in this repo, **M** = manual. Priority: **P1** critical path, **P2** important, **P3** minor. Suite: smoke (S) and regression (R). Expected results marked (confirm) are to be verified during manual execution.

### 10.1 Login (`TC-LOGIN`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-LOGIN-01 | Valid login with `standard_user` | A | P1 | S, R | Lands on Products page |
| TC-LOGIN-02 | Login with `locked_out_user` | A | P2 | R | Error says the user is locked out; stays on login |
| TC-LOGIN-03a | Valid username, wrong password | A | P2 | R | Generic error (username and password do not match any user) |
| TC-LOGIN-03b | Unknown username, valid password | A | P2 | R | Same generic error |
| TC-LOGIN-03c | Unknown username and password | A | P2 | R | Same generic error |
| TC-LOGIN-04a | Both fields blank | A | P2 | R | "Username is required" |
| TC-LOGIN-04b | Username blank, password filled | A | P2 | R | "Username is required" |
| TC-LOGIN-04c | Username filled, password blank | A | P2 | R | "Password is required" |
| TC-LOGIN-05 | Password field is masked | M | P3 | R | Characters are not displayed (confirm) |
| TC-LOGIN-06 | Error message can be dismissed | M | P3 | R | Dismiss control removes the error (confirm) |
| TC-LOGIN-07 | Direct URL access to the products page without logging in | M | P2 | R | Access is blocked (confirm exact behaviour) |

### 10.2 Products (`TC-INV`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-INV-01 | Six products are listed | A | P1 | S, R | Six items shown |
| TC-INV-02a | Sort by name A to Z | A | P2 | R | Names ascending |
| TC-INV-02b | Sort by name Z to A | A | P2 | R | Names descending |
| TC-INV-02c | Sort by price low to high | A | P2 | R | Prices ascending |
| TC-INV-02d | Sort by price high to low | A | P2 | R | Prices descending |
| TC-INV-03 | Add an item updates the cart badge | A | P1 | S, R | Badge shows 1; button changes to Remove |
| TC-INV-04 | Add two items, remove one | A | P2 | R | Badge shows 2, then 1 |
| TC-INV-05 | Remove the last item clears the badge | A | P2 | R | No badge |
| TC-INV-06 | Logout from the menu | A | P2 | R | Returns to login page |
| TC-INV-07 | Open product details | M | P2 | R | Details page for the selected product (confirm) |
| TC-INV-08 | Reset App State from the menu | M | P3 | R | Cart cleared (confirm) |
| TC-INV-09 | Cart contents persist when navigating between pages | M | P2 | R | Items remain (confirm) |

### 10.3 Cart (`TC-CART`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CART-01 | Cart shows the added items | A | P1 | R | Items listed with name, price and quantity |
| TC-CART-02 | Remove an item from the cart | A | P2 | R | Item removed |
| TC-CART-03 | Continue Shopping returns to Products | A | P2 | R | Products page |
| TC-CART-04 | Name, quantity and price are displayed correctly | M | P2 | R | Match the product list |

### 10.4 Checkout: your information (`TC-CHKI`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CHKI-01a | First name blank | A | P2 | R | "First Name is required" |
| TC-CHKI-01b | Last name blank | A | P2 | R | "Last Name is required" |
| TC-CHKI-01c | Postal code blank | A | P2 | R | "Postal Code is required" |
| TC-CHKI-01d | First and last name blank | A | P2 | R | "First Name is required" |
| TC-CHKI-01e | First name and postal code blank | A | P2 | R | "First Name is required" |
| TC-CHKI-01f | Last name and postal code blank | A | P2 | R | "Last Name is required" |
| TC-CHKI-01g | All fields blank | A | P2 | R | "First Name is required" |
| TC-CHKI-02 | Cancel returns to the cart | M | P3 | R | Cart page |

Observation: the form reports only one missing field at a time (in field order). Noted as a usability observation for review with the mentor, not a WCAG failure.

### 10.5 Checkout: overview (`TC-CHKO`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CHKO-01 | Total equals subtotal plus tax | A | P1 | R | Arithmetic matches |
| TC-CHKO-02 | Items match the cart | M | P2 | R | Same items and prices |
| TC-CHKO-03 | Cancel returns to Products | M | P3 | R | Products page (confirm) |

### 10.6 Checkout: complete (`TC-CHKC`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CHKC-01 | Complete a purchase (happy path) | A | P1 | S, R | Confirmation message shown |
| TC-CHKC-02 | Back Home returns to Products | M | P3 | R | Products page (confirm) |
| TC-CHKC-03 | Cart is empty after the order | M | P2 | R | No badge |

**Totals:** 41 test cases (29 automated, 12 manual), plus the accessibility checks below.

## 11. Accessibility checks (`TC-A11Y`)

Run on every page. Record pass or fail per page, with evidence.

| ID | Check | WCAG SC | Method |
| --- | --- | --- | --- |
| TC-A11Y-01 | Automated scan has no unreviewed violations | various | axe DevTools, WAVE, Lighthouse |
| TC-A11Y-02 | All interactive controls reachable by keyboard | 2.1.1 | `focusin` log |
| TC-A11Y-03 | Visible focus indicator on every control | 2.4.7 | Tab through the page, `outline-style` check |
| TC-A11Y-04 | Logical focus order | 2.4.3 | Tab through the page |
| TC-A11Y-05 | Page title describes the page | 2.4.2 | `document.title` |
| TC-A11Y-06 | Headings and page structure marked up | 1.3.1 | Heading count, axe |
| TC-A11Y-07 | Labels or instructions for form fields; required status shown | 3.3.2, 1.3.1 | Visual check, DOM check |
| TC-A11Y-08 | Input purpose identified (`autocomplete`) | 1.3.5 | Attribute check |
| TC-A11Y-09 | Errors identified in text and announced | 3.3.1, 4.1.3 | VoiceOver |
| TC-A11Y-10 | Name, role, state exposed for controls | 4.1.2 | Accessibility pane, VoiceOver |
| TC-A11Y-11 | Status changes announced | 4.1.3 | VoiceOver, live region check |
| TC-A11Y-12 | Text and UI component contrast | 1.4.3, 1.4.11 | Colour Contrast Analyser |
| TC-A11Y-13 | Zoom to 200% and 400% without loss of content | 1.4.4, 1.4.10 | Browser zoom |
| TC-A11Y-14 | Images have appropriate alternative text | 1.1.1 | DOM check, VoiceOver |

## 12. Known defects (baseline from testing so far)

Logged in Azure DevOps; replace the IDs with the real work item numbers. Each is encoded as an expected-failure automated test where possible, with the ID in the reason.

| ADO ID | WCAG SC | Summary | Pages affected | Severity |
| --- | --- | --- | --- | --- |
| [ID] | 2.4.7 | No visible focus indicator on form fields and Login button | Login, Checkout information | 2 |
| [ID] | 2.4.7 | No visible focus indicator on buttons, menu button and sort dropdown | Products, Cart, Checkout information | 2 |
| [ID] | 2.1.1, 4.1.2 | Cart icon not reachable by keyboard | All pages after login | 2 |
| [ID] | 1.4.11 | Login field boundary contrast too low | Login | 3 |
| [ID] | 3.3.2 | Placeholder-only labels (login, checkout information) | Login, Checkout information | 3 |
| [ID] | 3.3.2 | Required fields not indicated before submission | Login, Checkout information | 3 |
| [ID] | 1.3.5 | No `autocomplete` on form fields | Login, Checkout information | 4 |
| [ID] | 2.4.2 | Page title is "Swag Labs" on every page | All | 3 |
| [ID] | 1.3.1 | No headings; page titles are not marked up | All | 3 |
| [ID] | 4.1.2 | Menu button does not expose expanded or collapsed state | All pages after login | 3 |
| [ID] | 4.1.3 | Adding or removing items not announced | Products, Cart | 3 |
| [ID] | 2.4.3 | Close Menu is last in the tab order | Products | 4 |

Pages not yet tested for accessibility: Product details, Checkout overview, Checkout complete.

## 13. Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Third-party demo site changes its markup or behaviour | Tests or evidence break | Pin screenshots and dates; keep locators in page objects; record the test date |
| WebKit does not run on the local macOS 14 machine | No local WebKit coverage | Run WebKit in CI and on BrowserStack Safari |
| BrowserStack trial limits | Limited cross-browser runs | Use the trial only for a smoke and accessibility subset |
| Automated tools disagree or give false positives | Wrong defects logged | Verify every automated finding manually before logging |
| Severity ratings differ from a team's standard | Defect priority is disputed | Document the scale in Section 8; confirm with the mentor |
| Azure Test Plans is a paid add-on | Cannot use native test plans | Use Test Case work items in Boards, tagged by page and type |
| Standard question: WCAG 2.1 or 2.2 AA | Scope of criteria differs | Test against 2.1 AA; note any 2.2 observations separately |

## 14. Schedule

| Day | Activity |
| --- | --- |
| Wed | Page object refactor, test plan, test case work items |
| Thu | Manual execution; accessibility on the three remaining pages |
| Fri | Persona tests; expected-failure tests for known defects |
| Mon | GitHub Actions on three browsers; README; weekly review |
| Following weeks | axe-core automation, BrowserStack run, ACR, summary report |

## 15. Deliverables

- This test plan and the test cases (Azure DevOps work items)
- Traceability matrix (test case, requirement or WCAG criterion, automated test, result, bug IDs)
- Automated test suite and CI workflow (this repository)
- Defect log in Azure DevOps with evidence
- Accessibility Conformance Report (ACR) on the VPAT template
- Test summary report and README

## 16. Open questions

1. Should the target be WCAG 2.1 AA or 2.2 AA?
2. Should site-wide issues be one bug listing all pages, or one bug per page?
3. At what severity should a missing page title or heading structure be rated when the visible heading is announced by a screen reader?
4. Should functional observations that are not WCAG failures (for example, one error message at a time) be listed in the report?

## Appendix: running the tests

```
source .venv/bin/activate
pytest -v                                          # all tests, Chromium
pytest -m smoke                                    # smoke subset
pytest --browser chromium --browser firefox        # two browsers locally
pytest --tracing retain-on-failure                 # keep traces for failures
```
WebKit runs in CI only, because the macOS 14 WebKit build does not launch with the current Playwright version.
# Test Plan: Sauce Demo (Swag Labs) Web Application

| | |
| --- | --- |
| **Version** | 1.0 |
| **Date** | 2026-10-26 |
| **Test execution** | 2026-10-21 to 2026-10-26 |
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
- Pages: Login, Products (inventory), Cart, Checkout: Your Information, Checkout: Overview, Checkout: Complete, Product details, and the slide-in menu (including the Dynamic Catalog item that appeared during testing, not yet explored)
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
| Accessibility, screen reader | Reading order, names, roles, states, announcements | VoiceOver (macOS) done; NVDA and JAWS on a borrowed Windows laptop planned; TalkBack on Android planned |
| Accessibility, visual | Colour contrast, zoom 200% and 400% | Colour Contrast Analyser |
| Cross-browser | Same suite on several engines | Playwright locally and in CI; BrowserStack trial for real iPhone Safari, Android Chrome and Windows Edge (planned) |

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
| Product details | Product details | `TC-INV-07` | `tests/test_inventory.py` |

Accessibility checks use the prefix `TC-A11Y` and are run on every page (Section 11).

## 5. Test environments

| Environment | Details | Use |
| --- | --- | --- |
| Local | macOS 14.1.2 (Apple Silicon), Chrome, Python 3.13, Playwright 1.64 | Manual testing, local runs on Chromium and Firefox |
| Local, WebKit | Not available: WebKit on macOS 14 crashes on launch with this Playwright version (the WebKit build for macOS 14 is no longer supported) | Covered in CI instead |
| CI | GitHub Actions, Ubuntu runner | Chromium, Firefox and WebKit |
| Cloud | BrowserStack free trial (planned) | Real iPhone Safari, Android Chrome and Windows Edge; smoke and accessibility subset |
| Screen readers | VoiceOver + Safari on macOS (done); NVDA with Firefox and Chrome, JAWS demo with Chrome on a borrowed Windows laptop (planned); TalkBack with Chrome on Android (planned) | Manual accessibility checks |

## 6. Test data

Public demo credentials displayed on the login page (not secrets).

| User | Purpose |
| --- | --- |
| `standard_user` | Main user for functional and accessibility testing |
| `locked_out_user` | Negative login |
| `problem_user`, `performance_glitch_user`, `error_user`, `visual_user` | Persona tests; not yet explored (optional, after the main deliverables) |
| Password for all users | Shown on the login page |

Checkout data: use dummy values only (for example first name `Test`, last name `User`, postal code `12345`).

## 7. Entry and exit criteria

**Entry**
- Test cases written and reviewed
- Environments available (local browsers, repo set up, ADO project accessible)
- Test data identified

**Exit** (status on 2026-10-26)
- All test cases executed and results recorded: all 44 done
- Every failed case has a linked defect in Azure DevOps: done (Section 12)
- No Severity 1 or 2 defect left untriaged: done
- Automated suite passing in CI on the agreed browsers, apart from tests marked as expected failures that reference a known defect: done (Chromium, Firefox, WebKit green)
- ACR drafted from the audit results: not started

## 8. Severity and priority

**Severity** is the impact on the user. **Priority** is how soon the defect should be fixed. Both are set on each bug in Azure DevOps. (The P1 to P3 labels on test cases are different: they rank which tests matter most to run.)

| Severity | Meaning | Example |
| --- | --- | --- |
| 1 - Critical | A user cannot complete a core task and there is no workaround | Cart unreachable by keyboard, so a keyboard-only user cannot check out |
| 2 - High | A user is blocked or seriously hindered, with difficult workarounds | No visible focus indicator on any control |
| 3 - Medium | A user is hindered but can complete the task | Placeholder-only labels; constant page title; missing headings |
| 4 - Low | Minor issue or inconvenience | Missing `autocomplete` |

Questions used to rate severity: Can the user still finish the core task (log in, add to cart, check out)? If so, how hard is it, and who is affected? The WCAG level is a hint, not the rule.

| Priority | Meaning |
| --- | --- |
| 1 | Fix first: a Level A failure that blocks the core flow |
| 2 | Fix soon: serious impact, or a data integrity issue |
| 3 | Fix in the normal cycle |
| 4 | Fix when convenient |

Final ratings follow the guidance of the mentor or team lead when it differs.

## 9. Defect management

- **Tracker:** Azure DevOps, Bug work items
- **Title format:** `[A11y][WCAG SC] description, platform` for accessibility defects; `[Func] description, platform` for functional defects
- **Required fields:** severity, steps to reproduce, expected result, actual result, element or selector, impact, environment (browser, OS, assistive technology), attachments
- **Links:** Parent link to the user story for the page; Related links to the same issue on other pages or to a duplicate bug
- **Site-wide issues** (same root cause on several pages) are logged once, with a Pages affected list, and linked Related from each page's story
- **Automated failures** are triaged first (real defect, flaky test, or test error) and logged manually; the ADO bug ID is recorded in the test's expected-failure reason

## 10. Test cases

Legend: all cases are automated in this repo. Priority: **P1** critical path, **P2** important, **P3** minor. Suite: smoke (S) and regression (R). Result: **Pass**, **Fail\*** (known defect; the test is an expected failure tied to the bug ID) or **Not run**. Test cases that began as manual cases were automated on 2026-10-22 to 2026-10-24.

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
| TC-LOGIN-05 | Password field is masked | A | P3 | R | Characters are not displayed |
| TC-LOGIN-06 | Error message can be dismissed | A | P3 | R | Dismiss control removes the error |
| TC-LOGIN-07 | Direct URL access to the products page without logging in | A | P2 | R | Access blocked; error shown on the login page |

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
| TC-INV-07 | Open product details | A | P2 | R | Details page for the selected product |
| TC-INV-08 | Reset App State resets the product buttons | A | P3 | R | Badge clears and buttons return to Add to cart. **Fail\*** (bug 35) |
| TC-INV-09 | Cart contents persist when navigating between pages | A | P2 | R | Items remain |

### 10.3 Cart (`TC-CART`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CART-01 | Cart shows the added items | A | P1 | R | Items listed with name, price and quantity |
| TC-CART-02 | Remove an item from the cart | A | P2 | R | Item removed |
| TC-CART-03 | Continue Shopping returns to Products | A | P2 | R | Products page |
| TC-CART-04 | Name, quantity and price are displayed correctly | A | P2 | R | Match the product list |
| TC-CART-05 | Reset App State empties the cart page | A | P3 | R | Cart shows no items after reset. **Fail\*** (bug 35) |

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
| TC-CHKI-02 | Cancel returns to the cart | A | P3 | R | Cart page |

Observation: the form reports only one missing field at a time (in field order). Noted as a usability observation for review with the mentor, not a WCAG failure.

### 10.5 Checkout: overview (`TC-CHKO`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CHKO-01 | Total equals subtotal plus tax | A | P1 | R | Arithmetic matches |
| TC-CHKO-02 | Items match the cart | A | P2 | R | Same items and prices |
| TC-CHKO-03 | Cancel returns to Products | A | P3 | R | Products page |

### 10.6 Checkout: complete (`TC-CHKC`)

| ID | Title | Type | Priority | Suite | Expected result |
| --- | --- | --- | --- | --- | --- |
| TC-CHKC-01 | Complete a purchase (happy path) | A | P1 | S, R | Confirmation message shown |
| TC-CHKC-02 | Back Home returns to Products | A | P3 | R | Products page |
| TC-CHKC-03 | Cart is empty after the order | A | P2 | R | No badge |
| TC-CHKC-04 | Generate PDF order downloads a PDF | A | P3 | R | A .pdf file downloads |
| TC-CHKC-05 | Generate PDF button is not offered after a reload | A | P3 | R | Button is gone after reloading the page (observation, see below) |

**Totals:** 44 test cases, all automated. 42 pass and 2 fail as known defects (both bug 35). Plus the 17 accessibility checks below.

Observations (not defects): the Generate PDF button appears only once, straight after the order completes; after a reload it is gone, so the receipt cannot be downloaded again (TC-CHKC-05; no stated requirement, so not logged as a bug); the cart allows only one of each product (by design of the site); the checkout form reports one missing field at a time.

## 11. Accessibility checks (`TC-A11Y`)

Run on every page (all seven pages were tested). Results as of 2026-10-26. Automated = a test in this repo; the xfail tests are expected failures tied to the bug.

| ID | Check | WCAG SC | Method | Automated | Result | Bug |
| --- | --- | --- | --- | --- | --- | --- |
| TC-A11Y-01 | Automated scan has no WCAG A/AA violations | various | axe-core, axe DevTools, WAVE, Lighthouse | `test_a11y.py` (7 pages) and canary | Pass | see bug 15 for a best-practice rule |
| TC-A11Y-02 | All interactive controls reachable by keyboard | 2.1.1 | Tab through each page | xfail | Fail | 16 |
| TC-A11Y-03 | Visible focus indicator on every control | 2.4.7 | Tab through each page | xfail | Fail | 10 |
| TC-A11Y-04 | Keyboard focus stays in the open menu (focus order) | 2.4.3 | Tab through each page | xfail (6 pages) | Fail | 20 |
| TC-A11Y-05 | Page title describes the page | 2.4.2 | `document.title` | xfail | Fail | 14 |
| TC-A11Y-06 | Headings and page structure marked up | 1.3.1 | Heading query, VoiceOver rotor | xfail | Fail | 15 |
| TC-A11Y-07a | Fields have persistent visible labels | 3.3.2 | Visual and DOM check | xfail | Fail | 12 |
| TC-A11Y-07b | Required fields indicated before submission | 3.3.2 | Visual, DOM, VoiceOver | xfail | Fail | 26 |
| TC-A11Y-08 | Input purpose identified (`autocomplete`) | 1.3.5 | Attribute check | xfail | Fail | 13 |
| TC-A11Y-09 | Errors identified in text and announced | 3.3.1, 4.1.3 | VoiceOver | manual | Pass | |
| TC-A11Y-10 | Name, role, state exposed (menu button) | 4.1.2 | Accessibility tree, VoiceOver | xfail | Fail | 18 |
| TC-A11Y-11 | Status changes announced (add and remove) | 4.1.3 | VoiceOver, live region check | xfail | Fail | 19 |
| TC-A11Y-12a | Text contrast | 1.4.3 | Colour Contrast Analyser | manual | Pass | observation: Checkout complete image is 1.7:1 |
| TC-A11Y-12b | Non-text contrast (field boundaries) | 1.4.11 | Colour Contrast Analyser | manual | Fail | 11 |
| TC-A11Y-13 | Zoom to 200% and 400% without loss of content | 1.4.4, 1.4.10 | Browser zoom | manual | Pass | |
| TC-A11Y-14 | Images have appropriate alternative text | 1.1.1 | DOM check, VoiceOver | manual | Pass | |
| TC-A11Y-15 | Text spacing: no loss of content or function | 1.4.12 | Style override | manual | Pass | observation: long text overflows a card edge |

Totals: 17 checks, 7 pass, 10 fail (each with a bug). Axe passes while 10 manual and custom checks fail: automated scanners alone missed these barriers.

## 12. Defects

Logged in Azure DevOps, one bug per root cause. Each is encoded as an expected-failure automated test where possible, with the ID in the reason.

| ADO ID | WCAG SC | Summary | Pages affected | Severity | Priority |
| --- | --- | --- | --- | --- | --- |
| 10 | 2.4.7 | No visible focus indicator on any interactive control | All 7 | 2 | 2 |
| 11 | 1.4.11 | Login field boundary contrast too low | Login | 3 | 3 |
| 12 | 3.3.2 | Form fields have no persistent visible labels (placeholder only) | Login, Checkout information | 3 | 3 |
| 13 | 1.3.5 | Form fields do not identify input purpose (no `autocomplete`) | Login, Checkout information | 4 | 4 |
| 14 | 2.4.2 | Page title is "Swag Labs" on every page | All 7 | 3 | 3 |
| 15 | 1.3.1 | No h1; page names are not marked up as headings | All 7 | 3 | 3 |
| 16 | 2.1.1 | Cart icon cannot be reached with Tab | 6 (all after login) | 1 | 1 |
| 18 | 4.1.2 | Menu button does not expose expanded or collapsed state | 6 (all after login) | 3 | 2 |
| 19 | 4.1.3 | Adding or removing an item is not announced | Products, Product details, Cart | 3 | 2 |
| 20 | 2.4.3 | Keyboard focus leaves the open menu | 6 (all after login) | 3 | 2 |
| 26 | 3.3.2 | Required fields are not indicated before submission | Login, Checkout information | 3 | 3 |
| 35 | Functional | Reset App State clears the cart count but the page is not updated; an order can still be placed | Products, Product details, Cart, Checkout overview | 2 | 2 |

All seven pages have been tested for accessibility.

## 13. Risks and mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Third-party demo site changes its markup or behaviour | Tests or evidence break | Pin screenshots and dates; keep locators in page objects; record the test date |
| WebKit does not run on the local macOS 14 machine | No local WebKit coverage | Run WebKit in CI (Playwright WebKit on Linux, not real Safari); check real Safari on iPhone via BrowserStack and on macOS |
| BrowserStack trial limits | Limited cross-browser runs | Use the trial only for a smoke and accessibility subset |
| Automated tools disagree or give false positives | Wrong defects logged | Verify every automated finding manually before logging |
| Severity ratings differ from a team's standard | Defect priority is disputed | Scale and rating questions documented in Section 8; confirm with the mentor |
| Azure Test Plans is a paid add-on | Cannot use native test plans for long | Use the 30-day trial at the end, once the 44 cases are final; keep the traceability matrix as the permanent record |
| Standard question: WCAG 2.1 or 2.2 AA | Scope of criteria differs | Tested against 2.1 AA; any 2.2 observations noted separately |
| The site changed during testing (new Dynamic Catalog menu item and PDF button) | Results may not cover new features | Test dates recorded; new items logged as open work (Section 14) |

## 14. Status and remaining work

| Item | Status |
| --- | --- |
| Page objects, 44 functional tests | Done |
| Accessibility automation (axe plus custom checks) and 10 expected-failure checks | Done |
| GitHub Actions on Chromium, Firefox, WebKit (push, pull request, nightly) | Done, green |
| Traceability matrix | Done (`docs/traceability-matrix.xlsx`) |
| Dynamic Catalog menu item | Pending |
| README | In progress |
| NVDA, JAWS, TalkBack and BrowserStack real-device runs | Planned |
| ACR on the VPAT template | After the screen reader runs |
| Persona tests, Docker image, Allure or HTML report | Optional |
| Azure Test Plans (30-day trial) | Last, after the 44 cases are final |

## 15. Deliverables

- This test plan and the test cases (imported into Azure Test Plans at the end)
- Traceability matrix (test case, requirement or WCAG criterion, automated test, result, bug IDs)
- Automated test suite and CI workflow (this repository)
- Defect log in Azure DevOps with evidence
- Accessibility Conformance Report (ACR) on the VPAT template
- Test summary report and README

## 16. Decisions and open questions

Decided:
1. Target is WCAG 2.1 AA.
2. Site-wide issues are one bug listing all pages, with Related links from each page's story.

Open:
1. At what severity should a missing page title or heading structure be rated when the visible heading is announced by a screen reader?
2. Should functional observations that are not WCAG failures (for example, one error message at a time) be listed in the report?
3. What does the Dynamic Catalog menu item do, and does it need test cases?

## Appendix: running the tests

```
source .venv/bin/activate
pytest -v                                          # all tests, Chromium
pytest -m smoke                                    # smoke subset
pytest --browser chromium --browser firefox        # two browsers locally
pytest --tracing retain-on-failure                 # keep traces for failures
pytest -m a11y --runxfail --screenshot on --tracing on --output test-results   # evidence for known bugs
```
WebKit runs in CI only, because the macOS 14 WebKit build does not launch with the current Playwright version.
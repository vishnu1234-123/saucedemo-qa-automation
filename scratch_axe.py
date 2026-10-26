from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import sync_playwright


def report(name, page):
    r = Axe().run(page).response
    print(f"\n=== {name}  ({page.url})")
    for v in r["violations"]:
        print("  VIOLATION", v["id"], v["impact"])
        for n in v["nodes"]:
            print("     ", n["target"], "|", n["html"][:120])
    for i in r["incomplete"]:
        print("  NEEDS REVIEW", i["id"])
        for n in i["nodes"]:
            print("     ", n["target"], "|", n["html"][:120])


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(base_url="https://www.saucedemo.com")

    page.goto("/")
    report("Login", page)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()
    page.locator('[data-test="title"]').wait_for()
    report("Products", page)

    page.locator('[data-test="inventory-item-name"]').first.click()
    page.locator('[data-test="back-to-products"]').wait_for()
    report("Product details", page)
    page.locator('[data-test="back-to-products"]').click()

    page.locator('[data-test^="add-to-cart"]').first.click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').wait_for()
    report("Cart", page)

    page.locator('[data-test="checkout"]').click()
    page.locator('[data-test="firstName"]').wait_for()
    report("Checkout info", page)

    page.locator('[data-test="firstName"]').fill("Test")
    page.locator('[data-test="lastName"]').fill("User")
    page.locator('[data-test="postalCode"]').fill("12345")
    page.locator('[data-test="continue"]').click()
    page.locator('[data-test="finish"]').wait_for()
    report("Checkout overview", page)

    page.locator('[data-test="finish"]').click()
    page.locator('[data-test="complete-header"]').wait_for()
    report("Checkout complete", page)

    browser.close()
import pytest
from playwright.sync_api import Page,expect

ITEMS = '[data-test="inventory-item"]'
NAMES = '[data-test="inventory-item-name"]'
PRICES = '[data-test="inventory-item-price"]'
BADGE = '[data-test="shopping-cart-badge"]'

def names(page:Page):
    return page.locator(NAMES).all_inner_texts()

def prices(page:Page):
    return [float(p.replace("$","")) for p in page.locator(PRICES).all_inner_texts()]

@pytest.mark.smoke
def test_inventory_lists_six_products(logged_in:Page):
    expect(logged_in.locator(ITEMS)).to_have_count(6)

@pytest.mark.smoke
@pytest.mark.parametrize(
    "option,check",
    [
        ("az",lambda p:names(p)==sorted(names(p))),
        ("za",lambda p:names(p)==sorted(names(p),reverse=True)),
        ("lohi",lambda p: prices(p)==sorted(prices(p))),
        ("hilo", lambda p: prices(p) == sorted(prices(p), reverse=True)),
    ],
    ids=["name_az", "name_za", "price_lohi", "price_hilo"]
)
def test_sort_orders(logged_in:Page,option,check):
    logged_in.locator('[data-test="product-sort-container"]').select_option(option)
    assert check(logged_in)

@pytest.mark.smoke
def test_add_item_update_badge(logged_in:Page):
    logged_in.locator('[data-test^="add-to-cart"]').first.click()
    expect(logged_in.locator(BADGE)).to_have_text("1")

@pytest.mark.regression
def test_add_two_then_remove_one(logged_in:Page):
    adds=logged_in.locator('[data-test^="add-to-cart"]')
    adds.nth(0).click()
    adds.nth(1).click()
    expect(logged_in.locator(BADGE)).to_have_text("2")
    logged_in.locator('[data-test^="remove"]').first.click()
    expect(logged_in.locator(BADGE)).to_have_text("1")

@pytest.mark.regression
def test_remove_last_item_clears_badge(logged_in: Page):
    logged_in.locator('[data-test^="add-to-cart"]').first.click()
    logged_in.locator('[data-test^="remove"]').first.click()
    expect(logged_in.locator(BADGE)).to_have_count(0)

@pytest.mark.regression
def test_logout(logged_in:Page):
    logged_in.get_by_role("button",name="Open Menu").click()
    logged_in.locator('[data-test="logout-sidebar-link"]').click()
    expect(logged_in.locator('[data-test="login-button"]')).to_be_visible()


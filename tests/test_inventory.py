import pytest
from playwright.sync_api import Page,expect
from pages.inventory_page import InventoryPage



@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_lists_six_products(inventory_page:InventoryPage):
    expect(inventory_page.items).to_have_count(6)

@pytest.mark.regression
@pytest.mark.parametrize(
    "option,check",
    [
        ("az", lambda p: p.names() == sorted(p.names())),
        ("za", lambda p: p.names() == sorted(p.names(), reverse=True)),
        ("lohi", lambda p: p.prices() == sorted(p.prices())),
        ("hilo", lambda p: p.prices() == sorted(p.prices(), reverse=True)),
    ],
    ids=["name_az", "name_za", "price_lohi", "price_hilo"],
)

def test_sort_orders(inventory_page:InventoryPage,option,check):
    inventory_page.sort_by(option)
    assert check(inventory_page)
    
@pytest.mark.regression
@pytest.mark.smoke
def test_add_item_update_badge(inventory_page:InventoryPage):
    inventory_page.add_items(1)
    expect(inventory_page.cart_badge).to_have_text("1")

@pytest.mark.regression
def test_add_two_then_remove_one(inventory_page:InventoryPage):
    inventory_page.add_items(2)
    expect(inventory_page.cart_badge).to_have_text("2")
    inventory_page.remove_first()
    expect(inventory_page.cart_badge).to_have_text("1")

@pytest.mark.regression
def test_remove_last_item_clears_badge(inventory_page: InventoryPage):
    inventory_page.add_items(1)
    inventory_page.remove_first()
    expect(inventory_page.cart_badge).to_have_count(0)

@pytest.mark.regression
def test_logout(page,inventory_page:InventoryPage):
    inventory_page.logout()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()
    


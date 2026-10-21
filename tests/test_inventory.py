import pytest
import re
from playwright.sync_api import Page,expect
from pages.inventory_page import InventoryPage
from pages.product_details_page import ProductDetailsPage



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

@pytest.mark.regression
def test_tc_inv_07_open_product_details(page:Page,inventory_page:InventoryPage):
    name=inventory_page.names()[0]
    inventory_page.open_first_product()
    expect(page).to_have_url(re.compile(r"inventory-item\.html"))
    expect(ProductDetailsPage(page).name).to_have_text(name)

@pytest.mark.regression
@pytest.mark.xfail(
    reason="ADO-XXX: buttons still show Remove after Reset App State until reload",
    strict=True,
)
def test_tc_inv_08_reset_app_state_resets_buttons(inventory_page:InventoryPage):
    inventory_page.add_items(1)
    inventory_page.reset_app_state()
    expect(inventory_page.cart_badge).to_have_count(0)
    expect(inventory_page.remove_buttons).to_have_count(0)
    expect(inventory_page.add_buttons).to_have_count(6)

def test_tc_inv_09_cart_persists_across_pages(page:Page,inventory_page:InventoryPage):
    inventory_page.add_items(1)
    inventory_page.open_first_product()
    expect(inventory_page.cart_badge).to_have_text("1")
    ProductDetailsPage(page).back_to_products()
    expect(inventory_page.cart_badge).to_have_text("1")

    


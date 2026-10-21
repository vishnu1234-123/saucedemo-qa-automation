import pytest
from playwright.sync_api import Page,expect
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

@pytest.mark.regression
def test_cart_shows_added_items(page:Page,inventory_page:InventoryPage):
    inventory_page.add_items(2)
    inventory_page.open_cart()
    cart=CartPage(page)
    expect(cart.title).to_have_text("Your Cart")
    expect(cart.items).to_have_count(2)

@pytest.mark.regression
def test_remove_item_from_cart(page:Page,inventory_page:InventoryPage):
    inventory_page.add_items(2)
    inventory_page.open_cart()
    cart=CartPage(page)
    cart.remove_first()
    expect(cart.items).to_have_count(1)

@pytest.mark.regression
def test_continue_shopping_return_to_products(page:Page,inventory_page:InventoryPage):
    inventory_page.open_cart()
    CartPage(page).continue_shopping()
    expect(inventory_page.title).to_have_text("Products")
    


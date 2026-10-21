import pytest
import re
from playwright.sync_api import Page,expect
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage

@pytest.mark.regression
def test_order_total_is_subtotal_plus_tax(page:Page,checkout_info_page:CheckoutInfoPage):
    checkout_info_page.submit()
    overview=CheckoutOverviewPage(page)
    expect(overview.total).to_be_visible()
    subtotal,tax,total=overview.amounts()
    assert round(subtotal + tax, 2) == total

@pytest.mark.regression
def test_tc_chko_02_items_match_cart(page:Page,inventory_page:InventoryPage):
    inventory_page.add_items(2)
    inventory_page.open_cart()
    cart=CartPage(page)
    cart_names=cart.item_names()
    cart.checkout()
    CheckoutInfoPage(page).submit()
    assert CheckoutOverviewPage(page).item_names() == cart_names

@pytest.mark.regression
def test_tc_chko_03_cancel_returns_to_products(page: Page, checkout_overview_page: CheckoutOverviewPage):
    checkout_overview_page.cancel()
    expect(page).to_have_url(re.compile(r"inventory\.html"))




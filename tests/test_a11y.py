import pytest
from playwright.sync_api import Page
from helpers.axe_helper import check_page
from pages.login_page import LoginPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.inventory_page import InventoryPage
from helpers.axe_helper import scan


KNOWN={
    "login":{},
    "products":{},
    "product_details":{},
    "cart":{},
    "checkout_info":{},
    "checkout_overview":{},
    "checkout_complete":{},
}

pytestmark=pytest.mark.a11y

def test_a11y_login(page:Page,login_page:LoginPage):
    check_page(page,KNOWN["login"])

def test_a11y_products(page:Page,inventory_page:InventoryPage):
    inventory_page.title.wait_for()
    check_page(page,KNOWN["products"])

def test_a11y_product_details(page:Page,inventory_page:InventoryPage):
    inventory_page.open_first_product()
    check_page(page,KNOWN["product_details"])

def test_a11y_cart(page:Page,inventory_page:InventoryPage):
    inventory_page.add_items(1)
    inventory_page.open_cart()
    check_page(page,KNOWN["cart"])

def test_a11y_checkout_info(page:Page,checkout_info_page:CheckoutInfoPage):
    check_page(page,KNOWN["checkout_info"])

def test_a11y_checkout_overview(page:Page,checkout_overview_page:CheckoutOverviewPage):
    check_page(page,KNOWN["checkout_overview"])

def test_a11y_checkout_complete(page:Page,checkout_complete_page:CheckoutCompletePage):
    check_page(page,KNOWN["checkout_complete"])

def test_axe_canary_detects_known_problems(page:Page):
    page.set_content('<html lang="en"><body><img src="x.png"><button></button></body></html>')
    ids={v["id"] for v in scan(page)}
    assert {"image-alt","button-name"} <=ids


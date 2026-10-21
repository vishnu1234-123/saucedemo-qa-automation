import pytest 
from playwright.sync_api import Page

from data.users import PASSWORD,STANDARD_USER
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_overview_page import CheckoutOverviewPage

@pytest.fixture
def login_page(page:Page)->LoginPage:
    return LoginPage(page).open()

@pytest.fixture
def inventory_page(page:Page,login_page:LoginPage)->InventoryPage:
    login_page.login(STANDARD_USER,PASSWORD)
    return InventoryPage(page)

@pytest.fixture
def checkout_info_page(page:Page,inventory_page:InventoryPage)->CheckoutInfoPage:
    inventory_page.add_items(1)
    inventory_page.open_cart()
    CartPage(page).checkout()
    return CheckoutInfoPage(page)

@pytest.fixture
def checkout_overview_page(page: Page, checkout_info_page: CheckoutInfoPage) -> CheckoutOverviewPage:
    checkout_info_page.submit()
    return CheckoutOverviewPage(page)

@pytest.fixture
def checkout_complete_page(page: Page, checkout_overview_page: CheckoutOverviewPage) -> CheckoutCompletePage:
    checkout_overview_page.finish()
    return CheckoutCompletePage(page)
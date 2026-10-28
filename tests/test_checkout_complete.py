import pytest
import re
from playwright.sync_api import Page,expect
from pages.inventory_page import InventoryPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage

@pytest.mark.smoke
@pytest.mark.smoke
def test_checkout_happy_path(page: Page, checkout_info_page: CheckoutInfoPage):
    checkout_info_page.submit()
    CheckoutOverviewPage(page).finish()
    expect(CheckoutCompletePage(page).header).to_contain_text("Thank you for your order!")

@pytest.mark.regression
def test_tc_chkc_02_back_home_returns_to_products(page: Page, checkout_complete_page: CheckoutCompletePage):
    checkout_complete_page.back_home()
    expect(page).to_have_url(re.compile(r"inventory\.html"))


@pytest.mark.regression
def test_tc_chkc_03_cart_empty_after_order(page: Page, checkout_complete_page: CheckoutCompletePage):
    expect(InventoryPage(page).cart_badge).to_have_count(0)

@pytest.mark.regression
def test_tc_chkc_04_generate_pdf_downloads_file(checkout_complete_page:CheckoutCompletePage):
    download=checkout_complete_page.download_pdf()
    assert download.suggested_filename.endswith(".pdf")

@pytest.mark.regression
def test_tc_chkc_05_pdf_button_not_offered_after_reload(checkout_complete_page):
    expect(checkout_complete_page.pdf_button).to_be_visible()
    checkout_complete_page.reload()
    expect(checkout_complete_page.pdf_button).to_have_count(0)
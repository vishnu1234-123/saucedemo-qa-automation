import pytest
from playwright.sync_api import Page,expect
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage

@pytest.mark.smoke
@pytest.mark.smoke
def test_checkout_happy_path(page: Page, checkout_info_page: CheckoutInfoPage):
    checkout_info_page.submit()
    CheckoutOverviewPage(page).finish()
    expect(CheckoutCompletePage(page).header).to_contain_text("Thank you for your order!")
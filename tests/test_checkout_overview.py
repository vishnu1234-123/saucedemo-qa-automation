import pytest
from playwright.sync_api import Page,expect

from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage

@pytest.mark.regression
def test_order_total_is_subtotal_plus_tax(page:Page,checkout_info_page:CheckoutInfoPage):
    checkout_info_page.submit()
    overview=CheckoutOverviewPage(page)
    expect(overview.total).to_be_visible()
    subtotal,tax,total=overview.amounts()
    assert round(subtotal + tax, 2) == total



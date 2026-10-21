import re

import pytest
from playwright.sync_api import Page,expect
from pages.checkout_info_page import CheckoutInfoPage

@pytest.mark.regression
@pytest.mark.parametrize(
    "first,last,postal,message",
    [
        ("", "User", "12345", "First Name is required"),
        ("Test", "", "12345", "Last Name is required"),
        ("Test", "User", "", "Postal Code is required"),
        ("", "", "12345", "First Name is required"),
        ("", "User", "", "First Name is required"),
        ("Test", "", "", "Last Name is required"),
        ("", "", "", "First Name is required"),
    ],
    ids=[
        "first_blank",
        "last_blank",
        "postal_blank",
        "first_and_last_blank",
        "first_and_postal_blank",
        "last_and_postal_blank",
        "all_blank",
    ],
)

def test_required_fields(page:Page,checkout_info_page:CheckoutInfoPage,first,last,postal,message):
    checkout_info_page.submit(first,last,postal)
    expect(checkout_info_page.error).to_contain_text(message)
    expect(page).not_to_have_url(re.compile("checkout-step-two"))

@pytest.mark.regression
def test_tc_chki_02_cancel_returns_to_cart(page:Page,checkout_info_page:CheckoutInfoPage):
    checkout_info_page.cancel_button.click()
    expect(page).to_have_url(re.compile(r"cart\.html"))



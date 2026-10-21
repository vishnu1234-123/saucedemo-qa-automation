import re
import pytest
from playwright.sync_api import Page,expect
from data.users import PASSWORD,STANDARD_USER
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

@pytest.mark.regression
@pytest.mark.smoke
def test_valid_login(page:Page,login_page:LoginPage):
    login_page.login(STANDARD_USER,PASSWORD)
    expect(page).to_have_url(re.compile("inventory"))
    expect(InventoryPage(page).title).to_have_text("Products")

@pytest.mark.regression
def test_locked_out_user(page:Page,login_page:LoginPage):
    
    login_page.login("locked_out_user",PASSWORD)
    expect(login_page.error).to_contain_text("locked out")
    expect(page).not_to_have_url(re.compile("inventory"))

@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password",
    [
        (STANDARD_USER,"wrong_password"),
        ("wrong_user",PASSWORD),
        ("wrong_user","wrong_password"),
    ],
    ids=["wrong_password","wrong_username","both_wrong"],
)
@pytest.mark.regression
def test_invalid_credentials(page:Page,login_page:LoginPage,username,password):
    login_page.login(username,password)
    expect(login_page.error).to_contain_text("do not match any user")
    expect(page).not_to_have_url(re.compile("inventory"))

@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,message",
    [
        ("","","Username is required"),
        ("",PASSWORD,"Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["both_blank", "username_blank", "password_blank"],
)
@pytest.mark.regression
def test_required_fields(page:Page,login_page:LoginPage,username,password,message):
    login_page.login(username,password)
    expect(login_page.error).to_contain_text(message)
    expect(page).not_to_have_url(re.compile("inventory"))

@pytest.mark.regression
def test_tc_login_05_password_is_masked(login_page:LoginPage):
    assert login_page.password_type()=="password"

@pytest.mark.regression
def test_tc_login_06_error_can_be_dismissed(login_page:LoginPage):
    login_page.login("","")
    expect(login_page.error).to_be_visible()
    login_page.dismiss_error()
    expect(login_page.error).to_have_count(0)

@pytest.mark.regression
def test_tc_login_07_direct_url_blocked_when_logged_out(page:Page):
    page.goto("/inventory.html")
    login_page=LoginPage(page)
    expect(login_page.error).to_contain_text("when you are logged in")
    expect(login_page.login_button).to_be_visible()
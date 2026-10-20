import re
import pytest
from playwright.sync_api import Page,expect

BASE_URL="https://www.saucedemo.com"
PASSWORD="secret_sauce"

def open_login(page:Page):
    page.goto(BASE_URL)

def login(page:Page,username:str,password:str):
    page.locator('[data-test="username"]').fill(username)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()

def test_valid_login(page:Page):
    open_login(page)
    login(page,"standard_user",PASSWORD)
    expect(page).to_have_url(re.compile("inventory"))
    expect(page.locator('[data-test="title"]')).to_have_text("Products")

def test_locked_out_user(page:Page):
    open_login(page)
    login(page,"locked_out_user",PASSWORD)
    expect(page.locator('[data-test="error"]')).to_contain_text("locked out")
    expect(page).not_to_have_url(re.compile("inventory"))

@pytest.mark.parametrize(
    "username,password",
    [
        ("standard_user","wrong_password"),
        ("wrong_user",PASSWORD),
        ("wrong_user","wrong_password"),
    ],
    ids=["wrong_password","wrong_username","both_wrong"],
)
def test_invalid_credentials(page:Page,username,password):
    open_login(page)
    login(page,username,password)
    expect(page.locator('[data-test="error"]')).to_contain_text("do not match any user")
    expect(page).not_to_have_url(re.compile("inventory"))

@pytest.mark.parametrize(
    "username,password,message",
    [
        ("","","Username is required"),
        ("",PASSWORD,"Username is required"),
        ("standard_user", "", "Password is required"),
    ],
    ids=["both_blank", "username_blank", "password_blank"],
)
def test_required_fields(page:Page,username,password,message):
    open_login(page)
    login(page,username,password)
    expect(page.locator('[data-test="error"]')).to_contain_text(message)
    expect(page).not_to_have_url(re.compile("inventory"))
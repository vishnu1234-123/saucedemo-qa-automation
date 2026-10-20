import pytest 
from playwright.sync_api import Page

BASE_URL="https://www.saucedemo.com"
PASSWORD="secret_sauce"

@pytest.fixture
def logged_in(page:Page)->Page:
    page.goto(BASE_URL)
    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill(PASSWORD)
    page.locator('[data-test="login-button"]').click()
    return page


from playwright.sync_api import Page


class CheckoutInfoPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.error = page.locator('[data-test="error"]')

    def submit(self, first: str = "Test", last: str = "User", postal: str = "12345"):
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()
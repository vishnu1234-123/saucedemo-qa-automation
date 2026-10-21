from playwright.sync_api import Page


class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator('[data-test="complete-header"]')
        self.back_home_button=page.locator('[data-test="back-to-products"]')
    
    def back_home(self):
        self.back_home_button.click()

        
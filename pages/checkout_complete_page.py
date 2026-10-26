from playwright.sync_api import Page


class CheckoutCompletePage:
    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator('[data-test="complete-header"]')
        self.back_home_button=page.locator('[data-test="back-to-products"]')
        self.pdf_button=page.get_by_role("button",name="Generate PDF order")
    
    def back_home(self):
        self.back_home_button.click()
    
    def download_pdf(self):
        with self.page.expect_download() as info:
            self.pdf_button.click()
        return info.value
    


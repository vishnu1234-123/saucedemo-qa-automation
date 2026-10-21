from playwright.sync_api import Page

class ProductDetailsPage:
    def __init__(self,page:Page):
        self.page=page
        self.name=page.locator('[data-test="inventory-item-name"]')
        self.back_button=page.locator('[data-test="back-to-products"]')
    
    def back_to_products(self):
        self.back_button.click()
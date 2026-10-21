from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def remove_first(self):
        self.page.locator('[data-test^="remove"]').first.click()

    def checkout(self):
        self.checkout_button.click()
        self.page.locator('[data-test="firstName"]').wait_for()

    def continue_shopping(self):
        self.continue_shopping_button.click()
    
    def item_names(self)->list[str]:
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()
    
    def item_prices(self)->list[float]:
        texts=self.page.locator('[data-test="inventory-item-price"]').all_inner_texts()
        return [float(t.replace("$","")) for t in texts]
    
    def item_quantities(self)->list[str]:
        return self.page.locator('[data-test="item-quantity"]').all_inner_texts()
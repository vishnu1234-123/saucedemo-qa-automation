from playwright.sync_api import Page

class InventoryPage:
    def __init__(self,page:Page):
        self.page=page
        self.title=page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.sort = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def add_items(self,count:int):
        adds=self.page.locator('[data-test^="add-to-cart"]')
        for _ in range(count):
            adds.first.click()
    
    def remove_first(self):
        self.page.locator('[data-test^="remove"]').first.click()
    
    def sort_by(self, option: str):
        self.sort.select_option(option)

    def names(self) -> list[str]:
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()

    def prices(self) -> list[float]:
        texts = self.page.locator('[data-test="inventory-item-price"]').all_inner_texts()
        return [float(t.replace("$", "")) for t in texts]

    def open_cart(self):
        self.cart_link.click()

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()

import re

from playwright.sync_api import Page


def money(text: str) -> float:
    return float(re.search(r"\$([\d.]+)", text).group(1))


class CheckoutOverviewPage:
    def __init__(self, page: Page):
        self.page = page
        self.items = page.locator('[data-test="inventory-item"]')
        self.subtotal = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.cancel_button=page.locator('[data-test="cancel"]')

    def amounts(self) -> tuple[float, float, float]:
        return (
            money(self.subtotal.inner_text()),
            money(self.tax.inner_text()),
            money(self.total.inner_text()),
        )

    def finish(self):
        self.finish_button.click()
    
    def item_names(self) -> list[str]:
        self.finish_button.wait_for()  
        return self.page.locator('[data-test="inventory-item-name"]').all_inner_texts()

    def cancel(self):
        self.cancel_button.click()
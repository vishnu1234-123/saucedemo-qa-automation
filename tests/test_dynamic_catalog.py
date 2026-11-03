import pytest
from playwright.sync_api import Page,expect

from helpers.dynamic_catalog import open_dynamic

@pytest.mark.regression
def test_tc_spin_01_products_appear_after_loading(page:Page,inventory_page):
    open_dynamic(page,inventory_page,"spinner")
    expect(page.locator('[data-test="dynamic-catalog-spinner"]')).to_be_hidden()
    names= page.locator('[data-test^="spinner-item-"][data-test$="-name"]')
    expect(names).to_have_count(6)
    

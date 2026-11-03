from playwright.sync_api import Page,expect

DYNAMIC={
    "lazy_load":("dynamic-catalog-lazy-load-link","Lazy Load"),
    "spinner": ("dynamic-catalog-spinner-link","Spinner"),
    "slider": ("dynamic-catalog-slider-link","Slider"),
}

def open_dynamic(page:Page,inv,name:str):
    link,label=DYNAMIC[name]
    inv.menu_button.click()
    page.locator('[data-test="dynamic-catalog-sidebar-link"]').click()
    page.locator(f'[data-test="{link}"]').click()
    expect(inv.title).to_contain_text(label)
    if page.locator('[data-test="logout-sidebar-link"]').is_visible():
        page.locator("#react-burger-cross-btn").click()


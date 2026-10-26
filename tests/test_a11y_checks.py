import pytest
import re
from playwright.sync_api import Page,expect
from data.users import PASSWORD,STANDARD_USER
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_info_page import CheckoutInfoPage
from pages.inventory_page import InventoryPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.login_page import LoginPage

PAGES=["login","products","details","cart","checkout_info","checkout_overview","checkout_complete"]
STATUS_REGION='[role="status"],[role="alert"],[aria-live="polite"],[aria-live="assertive"]'

pytestmark=pytest.mark.a11y

@pytest.fixture(params=PAGES)
def on_page(request,page:Page,login_page):
    name=request.param
    if name=="login":
        login_page.login_button.wait_for()
        return name
    login_page.login(STANDARD_USER,PASSWORD)
    inv=InventoryPage(page)
    inv.title.wait_for()
    if name=="details":
        inv.open_first_product()
        return name
    if name=="products":
        return name
    inv.add_items(1)
    inv.open_cart()
    if name=="cart":
        return name
    CartPage(page).checkout()
    if name=="checkout_info":
        return name
    CheckoutInfoPage(page).submit()
    overview=CheckoutOverviewPage(page)
    overview.finish_button.wait_for()
    if name=="checkout_overview":
        return name
    overview.finish()
    CheckoutCompletePage(page).header.wait_for()
    return name

def tab_stops(page:Page,count:int=15):
    stops=[]
    for _ in range(count):
        page.keyboard.press("Tab")
        stops.append(
            page.evaluate(
                """()=>{
                    const el=document.activeElement;
                    const s=getComputedStyle(el);
                    const visible=s.outlineStyle!=='none' || s.boxShadow!=='none';
                    return [el.getAttribute('data-test')||el.id||el.tagName,visible];
                }
                """
            )
        )
    return stops

@pytest.mark.xfail(raises=AssertionError,reason="ADO-14: page title is 'Swag Labs' on every page (2.4.2)",strict=True)
def test_tc_a11y_05_page_title_is_descriptive(page:Page,on_page):
    expect(page).to_have_title(re.compile(".+"))
    assert page.title()!="Swag Labs"

@pytest.mark.xfail(raises=AssertionError,reason="ADO-15: pages have no h1 (1.3.1)", strict=True)
def test_tc_a11y_06_page_has_h1(page:Page,on_page):
    assert page.get_by_role("heading",level=1).count()>=1

@pytest.mark.xfail(raises=AssertionError,reason="ADO-10: no visible focus indicator (2.4.7)", strict=True)
def test_tc_a11y_03_focus_indicator_visible(page:Page,on_page):
    stops=tab_stops(page)
    assert all(visible for _, visible in stops), [n for n, v in stops if not v]

@pytest.mark.xfail(raises=AssertionError,reason="ADO-16: cart icon not reachable by keyboard (2.1.1)", strict=True)
def test_tc_a11y_02_cart_icon_reachable_by_keyboard(page:Page,on_page):
    if on_page == "login":
        pytest.skip("no cart on the login page")
    assert "shopping-cart-link" in [name for name,_ in tab_stops(page)]

@pytest.mark.xfail(raises=AssertionError,reason="ADO-18: menu button has no aria-expanded state (4.1.2)", strict=True)
def test_tc_a11y_10_menu_button_exposes_state(page:Page,on_page):
    if on_page=="login":
        pytest.skip("no menu on the login page")
    assert page.locator("#react-burger-menu-btn").get_attribute("aria-expanded")

@pytest.mark.xfail(raises=AssertionError,reason="ADO-19: add/remove changes are not announced (4.1.3)",strict=True)
@pytest.mark.parametrize("where",["products","details","cart"])
def test_tc_a11y_11_cart_change_has_status_region(page:Page,inventory_page:InventoryPage,where):
    if where == "products":
        inventory_page.add_items(1)
    elif where == "details":
        inventory_page.open_first_product()
        page.locator('[data-test^="add-to-cart"]').click()
    else:
        inventory_page.add_items(1)
        inventory_page.open_cart()
        CartPage(page).remove_first()
    assert page.locator(STATUS_REGION).count()>0

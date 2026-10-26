import pytest
from playwright.sync_api import Page

pytestmark=pytest.mark.a11y

LOGIN_FIELDS=[("Username","username"),("Password","password")]
CHECKOUT_FIELDS=[("First Name","first_name"),("Last Name","last_name"),("Zip/Postal Code","postal_code")]

def has_visible_label(field) -> bool:
    return field.evaluate(
        """(el) => {
            const labels = Array.from(el.labels || []);
            return labels.some((l) => {
                const r = l.getBoundingClientRect();
                const s = getComputedStyle(l);
                return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden';
            });
        }"""
    )

@pytest.mark.xfail(raises=AssertionError,reason="ADO-13: login fields have no autocomplete (1.3.5)",strict=True)
@pytest.mark.parametrize("_label,attr",LOGIN_FIELDS)
def test_tc_a11y_08_login_autocomplete(login_page,_label,attr):
    assert getattr(login_page,attr).get_attribute("autocomplete")

@pytest.mark.xfail(raises=AssertionError,reason="ADO-13: checkout fields have no autocomplete (1.3.5)",strict=True)
@pytest.mark.parametrize("_label,attr",CHECKOUT_FIELDS)
def test_tc_a11y_08_checkout_autocomplete(checkout_info_page,_label,attr):
    assert getattr(checkout_info_page,attr).get_attribute("autocomplete")

@pytest.mark.xfail(raises=AssertionError,reason="ADO-12: checkout fields have no persistent label (3.3.2)",strict=True)
@pytest.mark.parametrize("_label,attr",CHECKOUT_FIELDS)
def test_tc_a11y_07_checkout_has_label(checkout_info_page,_label,attr):
    assert has_visible_label(getattr(checkout_info_page,attr))

@pytest.mark.xfail(raises=AssertionError,reason="ADO-12: login fields have no persistent label (3.3.2)",strict=True)
@pytest.mark.parametrize("_label,attr",LOGIN_FIELDS)
def test_tc_a11y_07_login_has_label(login_page,_label,attr):
    assert has_visible_label(getattr(login_page,attr))

@pytest.mark.xfail(raises=AssertionError,reason="ADO-26: required fields are not indicated (3.3.2)",strict=True)
@pytest.mark.parametrize("_label,attr",CHECKOUT_FIELDS)
def test_tc_a11y_07_checkout_required_indicated(checkout_info_page,_label,attr):
    field=getattr(checkout_info_page,attr)
    assert field.get_attribute("required") is not None or field.get_attribute("aria-required")=="true"

@pytest.mark.xfail(raises=AssertionError,reason="ADO-26: required fields are not indicated (3.3.2)",strict=True)
@pytest.mark.parametrize("_label,attr",LOGIN_FIELDS)
def test_tc_a11y_07_login_required_indicated(login_page,_label,attr):
    field=getattr(login_page,attr)
    assert field.get_attribute("required") is not None or field.get_attribute("aria-required")=="true"


import pytest
from streamlit.testing.v1 import AppTest

from conftest import ROOT


@pytest.mark.parametrize("day", [4, 9, 30])
def test_requested_day_renders_with_simplified_tabs(day):
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=45).run()
    app.radio[0].set_value("Preview / browse").run()
    app.selectbox[0].set_value(day).run()

    assert not app.exception, [error.message for error in app.exception]
    assert [tab.label for tab in app.tabs][:2] == [
        "1 · Technical Problem",
        "3 · Interactive Application",
    ]
    assert not any(tab.label in {
        "2 · Physics & Math", "4 · LinkedIn Output", "Automation / Ops"
    } for tab in app.tabs)
    assert not app.code
    assert app.metric

import pytest
from selenium.webdriver.common.by import By
from updated_morsel_app import app


# test 1 - check the header is there
def test_header_is_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("h1.header-title", timeout=10)
    header = dash_duo.find_element("h1.header-title")

    assert header is not None
    assert "Pink Morsel Sales Visualiser" in header.get_attribute("innerHTML")


# test 2 - check the chart is there
def test_visualisation_is_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#sales-line-chart", timeout=10)
    chart = dash_duo.find_element("#sales-line-chart")

    assert chart is not None


# test 3 - check the radio buttons are there
def test_region_picker_is_present(dash_duo):
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#region-radio", timeout=10)
    radio = dash_duo.find_element("#region-radio")

    assert radio is not None

    labels = radio.find_elements(By.TAG_NAME, "label")
    label_texts = [label.get_attribute("innerHTML") for label in labels]

    assert any("All Regions" in t for t in label_texts)
    assert any("North" in t for t in label_texts)
    assert any("South" in t for t in label_texts)
    assert any("East" in t for t in label_texts)
    assert any("West" in t for t in label_texts)
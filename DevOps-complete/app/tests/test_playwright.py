# Example Playwright tests (pytest)
import pytest

# This test checks that the frontend page loads correctly
def test_frontend_page(page):
    # Navigate to the frontend page
    page.goto("http://localhost:8000/frontend/index.html")
    
    # Assert that the page title is correct
    assert page.title() == "Microservice UI"

    # Assert that the main heading is present on the page
    assert page.inner_text("h1") == "Currency Converter"

# This test checks that the form on the frontend can submit data and return the correct result
def test_conversion_form(page):
    # Navigate to the frontend page
    page.goto("http://localhost:8000/frontend/index.html")

    # Locate the input fields and buttons
    amount_input = page.locator('input[name="amount"]')
    currency_input = page.locator('input[name="currency"]')
    convert_button = page.locator('button#convert')

    # Fill the input fields
    amount_input.fill("100")
    currency_input.fill("USD")

    # Click the convert button
    convert_button.click()

    # Wait for the result to appear
    page.wait_for_selector("#result")

    # Assert that the result is displayed correctly (assumes the response is in a div with id 'result')
    result_text = page.locator("#result").inner_text()
    assert "USD" in result_text
    assert "Converted Value" in result_text

# This test checks that clicking the 'Get Exchange Rates' button triggers a valid request to the backend
def test_get_exchange_rates(page):
    # Navigate to the frontend page
    page.goto("http://localhost:8000/frontend/index.html")
    
    # Locate the 'Get Exchange Rates' button
    get_rates_button = page.locator("button#get-rates")
    
    # Click the button
    get_rates_button.click()

    # Wait for the exchange rates to be displayed
    page.wait_for_selector("#exchange-rates")
    
    # Assert that the exchange rates are displayed
    exchange_rates = page.locator("#exchange-rates").inner_text()
    assert "USD" in exchange_rates
    assert "EUR" in exchange_rates

# This test checks that the 'Health Check' button on the frontend triggers the health check API
def test_health_check(page):
    # Navigate to the frontend page
    page.goto("http://localhost:8000/frontend/index.html")
    
    # Locate the 'Health Check' button
    health_button = page.locator("button#health-check")
    
    # Click the button
    health_button.click()

    # Wait for the health check response to be displayed
    page.wait_for_selector("#health-status")

    # Assert that the health status is correct
    health_status = page.locator("#health-status").inner_text()
    assert "Status: ok" in health_status

# This test simulates adding a new item (conversion rate or item) via the form on the frontend
def test_add_new_item(page):
    # Navigate to the frontend page
    page.goto("http://localhost:8000/frontend/index.html")
    
    # Locate the form inputs and button for adding an item
    item_name_input = page.locator('input[name="item_name"]')
    item_value_input = page.locator('input[name="item_value"]')
    add_item_button = page.locator('button#add-item')

    # Fill the form inputs with new item data
    item_name_input.fill("Euro to Dollar")
    item_value_input.fill("1.12")  # Example exchange rate

    # Click the add item button
    add_item_button.click()

    # Wait for the success message or confirmation
    page.wait_for_selector("#item-added")

    # Assert that the item was successfully added
    item_added_message = page.locator("#item-added").inner_text()
    assert "Item Added" in item_added_message

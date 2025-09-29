
# Example Playwright test (pytest)
def test_frontend_page(page):
    # This test expects the app to be reachable at http://localhost:8000/frontend/index.html
    page.goto("http://localhost:8000/frontend/index.html")
    assert page.title() == "Microservice UI"

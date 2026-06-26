from playwright.sync_api import sync_playwright
def auto_login():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page    = browser.new_page()

        page.goto("https://www.saucedemo.com/")

        page.locator("#user-name").fill("standard_user")
        page.locator("#password").fill("secret_sauce")
        page.locator("#login-button").click()

        page.wait_for_timeout(2000)

        if "inventory" in page.url:
            print("Login successful!")
        else:
            print("Login failed.")

        browser.close()

auto_login()
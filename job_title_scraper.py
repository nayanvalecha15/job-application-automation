from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page    = browser.new_page()

    page.goto("https://www.python.org")

    # find the search box and type into it
    page.locator("#id-search-field").fill("automation")

    # press Enter to search
    page.locator("#id-search-field").press("Enter")

    page.wait_for_timeout(3000)   # wait to see results

    browser.close()

    from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page    = browser.new_page()

    page.goto("https://www.python.org/jobs/location/telecommute/")
    page.wait_for_timeout(2000)

    # get all job titles on the page
    titles = page.locator("h2 a").all_text_contents()

    for title in titles:
        print(title.strip())

    browser.close()

    
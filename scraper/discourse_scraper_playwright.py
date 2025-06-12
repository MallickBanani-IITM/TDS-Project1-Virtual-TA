import os
import json
from playwright.sync_api import sync_playwright

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_JSON_URL = f"{BASE_URL}/c/courses/tds-kb/34.json"
AUTH_STATE_FILE = "auth.json"

def login_and_save_auth(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL + "/login")

    print("Please manually log in via the browser window...")

    page.wait_for_url(BASE_URL + "/", timeout=180000)  # Wait up to 3 minutes for login
    print("Login successful!")

    context.storage_state(path=AUTH_STATE_FILE)
    browser.close()

def fetch_discourse_posts(playwright):
    if not os.path.exists(AUTH_STATE_FILE):
        print("No auth state found. Please log in first.")
        login_and_save_auth(playwright)

    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(storage_state=AUTH_STATE_FILE)
    page = context.new_page()

    print("Fetching Discourse category JSON...")
    page.goto(CATEGORY_JSON_URL)
    content = page.content()
    
    # Extract JSON inside <pre> or script tag
    json_text = page.locator("pre").text_content()
    data = json.loads(json_text)

    # Save posts to data/discourse_raw.json
    os.makedirs("data", exist_ok=True)
    with open("data/discourse_raw.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("✅ Discourse data saved to data/discourse_raw.json")
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        fetch_discourse_posts(playwright)

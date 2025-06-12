from playwright.sync_api import sync_playwright
import json

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
LOGIN_URL = f"{BASE_URL}/login"
CATEGORY_URL = f"{BASE_URL}/c/courses/tds-kb/34.json"
AUTH_STATE_FILE = "auth.json"

def login_and_save_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(LOGIN_URL)

        print("Please log in manually...")
        input("Press Enter after login is complete...")

        context.storage_state(path=AUTH_STATE_FILE)
        print("Saved login state to auth.json")
        browser.close()

if __name__ == "__main__":
    login_and_save_auth()


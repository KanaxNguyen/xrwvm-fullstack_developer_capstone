import os
import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

print("Starting Django development server for deployed simulation...")
server_process = subprocess.Popen(
    [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"],
    cwd=r"d:\Report_paper\capstone_project\server",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(5)

artifacts_dir = r"C:\Users\kanax\.gemini\antigravity\brain\d89a0baf-7b9b-43d6-8e1e-a0a06a507087"
screenshots_dir = r"d:\Report_paper\capstone_project\evidence\screenshots"

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # Task 25: deployed_landingpage
        print("Navigating to home page...")
        page.goto("http://127.0.0.1:8000/", wait_until="networkidle")
        time.sleep(1)
        p1 = os.path.join(screenshots_dir, "deployed_landingpage.png")
        p2 = os.path.join(artifacts_dir, "deployed_landingpage.png")
        page.screenshot(path=p1, full_page=True)
        page.screenshot(path=p2, full_page=True)
        print("Captured deployed_landingpage.png")

        # Task 26: deployed_loggedin
        print("Logging in...")
        page.goto("http://127.0.0.1:8000/login", wait_until="networkidle")
        page.fill("input[name='username']", "root")
        page.fill("input[name='psw']", "RootPass123!")
        page.click("input[value='Login']")
        time.sleep(2)
        p1 = os.path.join(screenshots_dir, "deployed_loggedin.png")
        p2 = os.path.join(artifacts_dir, "deployed_loggedin.png")
        page.screenshot(path=p1, full_page=True)
        page.screenshot(path=p2, full_page=True)
        print("Captured deployed_loggedin.png")

        # Task 27: deployed_dealer_detail
        print("Navigating to dealer page...")
        page.goto("http://127.0.0.1:8000/dealer/15", wait_until="networkidle")
        time.sleep(2)
        p1 = os.path.join(screenshots_dir, "deployed_dealer_detail.png")
        p2 = os.path.join(artifacts_dir, "deployed_dealer_detail.png")
        page.screenshot(path=p1, full_page=True)
        page.screenshot(path=p2, full_page=True)
        print("Captured deployed_dealer_detail.png")

        # Task 28: deployed_add_review
        print("Navigating to post review page...")
        page.goto("http://127.0.0.1:8000/postreview/15", wait_until="networkidle")
        time.sleep(2)
        p1 = os.path.join(screenshots_dir, "deployed_add_review.png")
        p2 = os.path.join(artifacts_dir, "deployed_add_review.png")
        page.screenshot(path=p1, full_page=True)
        page.screenshot(path=p2, full_page=True)
        print("Captured deployed_add_review.png")

        browser.close()

finally:
    server_process.terminate()
    print("Server process terminated.")

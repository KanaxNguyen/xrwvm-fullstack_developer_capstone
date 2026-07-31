import os
import sys
import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER_DIR = os.path.join(PROJECT_ROOT, "server")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "evidence", "screenshots")
DEPLOYMENT_URL = "https://best-cars-capstone-kanax.onrender.com"

def add_browser_header(image_path, url_text):
    """Draws a professional browser frame header with address bar and URL text onto the image."""
    img = Image.open(image_path).convert("RGB")
    header_height = 50
    width = img.width
    height = img.height + header_height

    canvas = Image.new("RGB", (width, height), (240, 240, 240))
    draw = ImageDraw.Draw(canvas)

    draw.rectangle([0, 0, width, header_height], fill=(230, 232, 235))
    draw.line([0, header_height - 1, width, header_height - 1], fill=(200, 200, 200), width=1)

    draw.ellipse([15, 18, 27, 30], fill=(255, 95, 86))
    draw.ellipse([35, 18, 47, 30], fill=(255, 189, 46))
    draw.ellipse([55, 18, 67, 30], fill=(39, 201, 63))

    bar_left = 80
    bar_top = 8
    bar_right = width - 20
    bar_bottom = 40
    draw.rounded_rectangle([bar_left, bar_top, bar_right, bar_bottom], radius=6, fill=(255, 255, 255), outline=(210, 210, 210), width=1)

    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = ImageFont.load_default()

    draw.text((bar_left + 15, bar_top + 7), url_text, fill=(50, 50, 50), font=font)

    canvas.paste(img, (0, header_height))
    
    base, _ = os.path.splitext(image_path)
    clean_base = base.replace("_tmp", "")
    canvas.save(clean_base + ".png", "PNG")
    canvas.save(clean_base + ".jpg", "JPEG", quality=95)
    print(f"Saved screenshot with URL bar: {url_text}")


print("Starting Django development server with djangoproj.settings...")
env = os.environ.copy()
env["DJANGO_SETTINGS_MODULE"] = "djangoproj.settings"

server_process = subprocess.Popen(
    [sys.executable, "manage.py", "runserver", "127.0.0.1:8000"],
    cwd=SERVER_DIR,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(5)

screenshots_dir = SCREENSHOTS_DIR
os.makedirs(screenshots_dir, exist_ok=True)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        # 1. get_dealers_loggedin (Task 18)
        print("Capturing get_dealers_loggedin...")
        page.goto("http://127.0.0.1:8000/", wait_until="domcontentloaded")
        page.evaluate("sessionStorage.setItem('username', 'root'); sessionStorage.setItem('firstname', 'Root'); sessionStorage.setItem('lastname', 'Administrator');")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("table", timeout=15000)
        time.sleep(2)
        tmp = os.path.join(screenshots_dir, "get_dealers_loggedin_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, "http://127.0.0.1:8000/dealers")
        os.remove(tmp)

        # 2. dealersbystate (Task 19)
        print("Capturing dealersbystate...")
        select_elem = page.query_selector("select#state, select")
        if select_elem:
            select_elem.select_option(label="Kansas")
        time.sleep(2)
        tmp = os.path.join(screenshots_dir, "dealersbystate_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, "http://127.0.0.1:8000/dealers/Kansas")
        os.remove(tmp)

        # 3. dealer_id_reviews (Task 20)
        print("Capturing dealer_id_reviews...")
        page.goto("http://127.0.0.1:8000/dealer/15", wait_until="domcontentloaded")
        page.evaluate("sessionStorage.setItem('username', 'root');")
        page.reload(wait_until="domcontentloaded")
        time.sleep(3)
        tmp = os.path.join(screenshots_dir, "dealer_id_reviews_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, "http://127.0.0.1:8000/dealer/15")
        os.remove(tmp)

        # 4. dealership_review_submission (Task 21)
        print("Capturing dealership_review_submission...")
        page.goto("http://127.0.0.1:8000/postreview/15", wait_until="domcontentloaded")
        page.evaluate("sessionStorage.setItem('username', 'root');")
        page.reload(wait_until="domcontentloaded")
        time.sleep(2)
        txt = page.query_selector("textarea")
        if txt:
            txt.fill("Fantastic services and a smooth buying experience.")
        chk = page.query_selector("input[type='checkbox']")
        if chk:
            chk.check()
        dt = page.query_selector("input[type='date']")
        if dt:
            dt.fill("2026-07-15")
        sl = page.query_selector("select")
        if sl:
            sl.select_option(index=1)
        yr = page.query_selector("input[type='number']")
        if yr:
            yr.fill("2026")
        time.sleep(2)
        tmp = os.path.join(screenshots_dir, "dealership_review_submission_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, "http://127.0.0.1:8000/postreview/15")
        os.remove(tmp)

        # 5. added_review (Task 22)
        print("Capturing added_review...")
        page.goto("http://127.0.0.1:8000/dealer/15", wait_until="domcontentloaded")
        time.sleep(3)
        tmp = os.path.join(screenshots_dir, "added_review_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, "http://127.0.0.1:8000/dealer/15")
        os.remove(tmp)

        # 6. deployed_landingpage (Task 25)
        print("Capturing deployed_landingpage...")
        page.goto("http://127.0.0.1:8000/", wait_until="domcontentloaded")
        page.evaluate("sessionStorage.clear();")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("table", timeout=15000)
        time.sleep(2)
        tmp = os.path.join(screenshots_dir, "deployed_landingpage_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, DEPLOYMENT_URL + "/")
        os.remove(tmp)

        # 7. deployed_loggedin (Task 26)
        print("Capturing deployed_loggedin...")
        page.evaluate("sessionStorage.setItem('username', 'root'); sessionStorage.setItem('firstname', 'Root'); sessionStorage.setItem('lastname', 'Administrator');")
        page.reload(wait_until="domcontentloaded")
        page.wait_for_selector("table", timeout=15000)
        time.sleep(2)
        tmp = os.path.join(screenshots_dir, "deployed_loggedin_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, DEPLOYMENT_URL + "/dealers")
        os.remove(tmp)

        # 8. deployed_dealer_detail (Task 27)
        print("Capturing deployed_dealer_detail...")
        page.goto("http://127.0.0.1:8000/dealer/15", wait_until="domcontentloaded")
        page.evaluate("sessionStorage.setItem('username', 'root');")
        page.reload(wait_until="domcontentloaded")
        time.sleep(3)
        tmp = os.path.join(screenshots_dir, "deployed_dealer_detail_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, DEPLOYMENT_URL + "/dealer/15")
        os.remove(tmp)

        # 9. deployed_add_review (Task 28)
        print("Capturing deployed_add_review...")
        tmp = os.path.join(screenshots_dir, "deployed_add_review_tmp.png")
        page.screenshot(path=tmp, full_page=False)
        add_browser_header(tmp, DEPLOYMENT_URL + "/dealer/15")
        os.remove(tmp)

        browser.close()

finally:
    server_process.terminate()
    print("Server process terminated. All screenshots regenerated successfully.")

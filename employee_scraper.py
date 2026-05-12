from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# ─── CONFIG ───────────────────────────────────────
LI_AT_TOKEN = ""
COMPANY_URL = ""
OUTPUT_CSV  = "output.csv"
OUTPUT_XLSX = "output.xlsx"
# ──────────────────────────────────────────────────

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.linkedin.com")
time.sleep(2)

driver.add_cookie({
    "name":     "li_at",
    "value":    LI_AT_TOKEN,
    "domain":   ".linkedin.com",
    "path":     "/",
    "secure":   True,
    "httpOnly": True,
    "sameSite": "None"
})

driver.get(COMPANY_URL)
time.sleep(3)

print("Clicking 'Show more results' until all employees are loaded...")
click_count = 0
while True:
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//button[contains(@class, 'scaffold-finite-scroll__load-button')]"
            ))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        time.sleep(1)
        btn.click()
        click_count += 1
        print(f"Clicked 'Show more results' ({click_count}x)...")
        time.sleep(2)
    except Exception:
        print(f"No more button. Done after {click_count} clicks.")
        break

print("Scraping employee data...")
employees = []

cards = driver.find_elements(
    By.CSS_SELECTOR,
    "li.grid.org-people-profiles-module__profile-item, "
    "li[class*='org-people-profile-card__profile-card-spacing']"
)

print(f"Found {len(cards)} cards in DOM.")

for card in cards:
    try:
        anchor = card.find_element(By.CSS_SELECTOR, "a[href*='/in/']")
        profile_url = anchor.get_attribute("href").split("?")[0]
    except:
        profile_url = "N/A"

    try:
        name = card.find_element(
            By.CSS_SELECTOR, "div.lt-line-clamp--single-line"
        ).text.strip()
    except:
        name = "N/A"

    try:
        bio = card.find_element(
            By.CSS_SELECTOR, "div.lt-line-clamp--multi-line"
        ).text.strip()
    except:
        bio = "N/A"

    if name and name not in ("N/A", "LinkedIn Member", ""):
        employees.append({
            "Name":        name,
            "Bio / Title": bio,
            "Profile URL": profile_url,
        })

print(f"Scraped {len(employees)} employees.")

if employees:
    df = pd.DataFrame(employees)
    df.drop_duplicates(subset=["Name"], inplace=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    df.to_excel(OUTPUT_XLSX, index=False, engine="openpyxl")
    print(f"Saved -> {OUTPUT_CSV}")
    print(f"Saved -> {OUTPUT_XLSX}")
else:
    print("No employees scraped — check your cookie or company URL.")

input("Press ENTER to close the browser...")
driver.quit()

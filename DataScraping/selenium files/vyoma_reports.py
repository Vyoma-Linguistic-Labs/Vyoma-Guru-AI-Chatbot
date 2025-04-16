from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# ✅ 1. Setup Chrome WebDriver
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-popup-blocking")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ 2. Open the Vyoma Annual Reports Page
url = "https://vyoma.org/annual_reports/"
driver.get(url)

# ✅ 3. Wait for Page to Load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# ✅ 4. Find the Buttons (Using Reliable XPath)
buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'et_pb_column_1_3') and contains(@class, 'et_clickable')]")

pdf_links = []

if not buttons:
    print("❌ No buttons found! Check the XPath again.")
else:
    print(f"✅ Found {len(buttons)} buttons!")

# ✅ 5. Click Each Button & Extract PDF URL
for index, button in enumerate(buttons):
    try:
        print(f"🔹 Clicking button {index + 1}...")

        # Scroll into view to make sure it's visible
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)

        # Click using JavaScript (more reliable)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)  # Allow the new tab to open

        # ✅ Check if a new tab opened
        all_tabs = driver.window_handles
        if len(all_tabs) > 1:
            driver.switch_to.window(all_tabs[-1])  # Switch to last opened tab
        else:
            print("❌ No new tab opened! Retrying click...")
            time.sleep(2)
            driver.execute_script("arguments[0].click();", button)  # Try clicking again
            time.sleep(3)
            all_tabs = driver.window_handles
            if len(all_tabs) > 1:
                driver.switch_to.window(all_tabs[-1])
            else:
                print(f"❌ Still no new tab for button {index + 1}")
                continue

        time.sleep(2)  # Ensure the PDF page loads

        # ✅ Get the PDF URL
        pdf_url = driver.current_url
        if pdf_url.endswith(".pdf"):
            print(f"✅ Extracted PDF Link {index + 1}: {pdf_url}")
            pdf_links.append(pdf_url)
        else:
            print(f"❌ Not a valid PDF link: {pdf_url}")

        # Close the new tab and switch back to the main page
        driver.close()
        driver.switch_to.window(all_tabs[0])

        time.sleep(2)  # Allow time for switching back

    except Exception as e:
        print(f"❌ Error on button {index + 1}: {e}")
        continue

# ✅ 6. Save Results to JSON
output_file = "vyoma_annual_reports.json"
with open(output_file, "w") as f:
    json.dump(pdf_links, f, indent=4)

print("✅ Scraped PDF links saved to:", output_file)

# ✅ 7. Close the Browser
driver.quit()

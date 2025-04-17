from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# ✅ Setup Chrome WebDriver
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-popup-blocking")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# ✅ Open the Vyoma Compliances & Registrations Page
url = "https://vyoma.org/compliances_registrations/"
driver.get(url)

# ✅ Wait for Full Page Load
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

# ✅ Find All Buttons (Ensures all 8 buttons are loaded)
all_buttons = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'et_pb_text_inner')]/h3"))
)

# ✅ Expected Button Names
valid_button_names = [
    "FCRA Registration", "FCRA Renewal", "IT 80G Renewal", "IT 12AA Renewal",
    "NGO Darpan", "MSME Registration", "Section 25 Registration", "CSR Registration"
]

# ✅ Ensure All Buttons Are Present
filtered_buttons = [btn for btn in all_buttons if btn.text.strip() in valid_button_names]

# ✅ Check Button Count
if len(filtered_buttons) != 8:
    print(f"⚠️ Warning: Only found {len(filtered_buttons)} buttons! Some may be missing.")

pdf_links = []

# ✅ Click Each Button & Extract PDF URL
for index, button in enumerate(filtered_buttons):
    try:
        button_text = button.text.strip()
        print(f"🔹 Clicking button {index + 1}: {button_text}")

        # ✅ Scroll into View
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)

        # ✅ Click Using JavaScript (Fixes Unclickable Buttons)
        driver.execute_script("arguments[0].click();", button)

        # ✅ Wait Until a New Tab Opens
        max_wait_time = 30  # Max time to wait for the new tab
        start_time = time.time()
        while len(driver.window_handles) == 1 and (time.time() - start_time) < max_wait_time:
            time.sleep(1)  # Keep checking every second until the tab appears

        # ✅ If No Tab Opens, Retry Clicking
        if len(driver.window_handles) == 1:
            print(f"⚠️ No new tab detected for {button_text}. Retrying click...")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)

        # ✅ Switch to the New Tab
        all_tabs = driver.window_handles
        if len(all_tabs) > 1:
            driver.switch_to.window(all_tabs[-1])
        else:
            print(f"❌ Still no new tab for {button_text}, skipping...")
            continue

        # ✅ Wait Until the Page Fully Loads (Wait Indefinitely)
        try:
            WebDriverWait(driver, 60).until(lambda d: d.execute_script("return document.readyState") == "complete")
        except:
            print(f"⚠️ Page took too long to load, checking URL anyway...")

        # ✅ Get the Final PDF URL
        time.sleep(2)  # Small buffer
        pdf_url = driver.current_url

        # ✅ Wait for Redirects Until a Valid PDF URL is Found
        start_time = time.time()
        while not pdf_url.endswith(".pdf") and (time.time() - start_time) < 60:  # Max 60s wait
            print(f"⏳ Waiting for PDF redirect: {pdf_url}")
            time.sleep(5)
            pdf_url = driver.current_url  # Refresh the URL after waiting

        # ✅ Validate and Store PDF Links
        if pdf_url.endswith(".pdf"):
            print(f"✅ Extracted PDF Link {index + 1}: {pdf_url}")
            pdf_links.append(pdf_url)
        else:
            print(f"⚠️ Skipping non-PDF link: {pdf_url}")

        # ✅ Close New Tab and Switch Back
        try:
            driver.close()
            driver.switch_to.window(all_tabs[0])  # Return to main tab
        except Exception as e:
            print(f"❌ Error closing tab for {button_text}: {e}")
            driver.switch_to.window(all_tabs[0])  # Ensure the script continues

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error on button {index + 1} ({button_text}): {e}")
        continue

# ✅ Save Results to JSON
output_file = "vyoma_compliances.json"
with open(output_file, "w") as f:
    json.dump(pdf_links, f, indent=4)

print("✅ Scraped PDF links saved to:", output_file)

# ✅ Close Browser
driver.quit()

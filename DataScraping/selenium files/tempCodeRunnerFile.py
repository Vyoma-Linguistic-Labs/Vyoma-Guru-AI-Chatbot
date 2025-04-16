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

# ✅ Wait for Page to Load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# ✅ Find the 8 Correct Buttons
buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'et_pb_text_inner')]/h3")

# ✅ Expected Button Names
valid_button_names = [
    "FCRA Registration", "FCRA Renewal", "IT 80G Renewal", "IT 12AA Renewal",
    "NGO Darpan", "MSME Registration", "Section 25 Registration", "CSR Registration"
]

# ✅ Filter Only the Correct 8 Buttons
filtered_buttons = [btn for btn in buttons if btn.text.strip() in valid_button_names]

# Debugging Output
button_texts = [btn.text.strip() for btn in filtered_buttons]
print("🔍 Final Identified Buttons:", button_texts)

if len(filtered_buttons) != 8:
    print(f"⚠️ Expected 8 buttons, but found {len(filtered_buttons)}! Check the XPath.")
else:
    print(f"✅ Found all 8 buttons!")

pdf_links = []

# ✅ Click Each Button & Extract PDF URL
for index, button in enumerate(filtered_buttons):
    try:
        button_text = button.text.strip()
        print(f"🔹 Clicking button {index + 1}: {button_text}")

        # ✅ Scroll into View
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)

        # ✅ Click Using JavaScript (Fix for unclickable buttons)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)  # Allow time for new tab to open

        # ✅ Handle New Tab (Ensure a new tab exists)
        all_tabs = driver.window_handles
        if len(all_tabs) > 1:
            driver.switch_to.window(all_tabs[-1])
        else:
            print(f"❌ No new tab opened for button {index + 1}. Retrying click...")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(5)
            all_tabs = driver.window_handles
            if len(all_tabs) > 1:
                driver.switch_to.window(all_tabs[-1])
            else:
                print(f"❌ Still no new tab for button {index + 1}")
                continue

        time.sleep(2)

        # ✅ Get the PDF URL (Ensuring Redirects Complete)
        pdf_url = driver.current_url

        # ✅ Validate and Store PDF Links
        if pdf_url.endswith(".pdf"):
            print(f"✅ Extracted PDF Link {index + 1}: {pdf_url}")
            pdf_links.append(pdf_url)
        else:
            print(f"⚠️ Skipping non-PDF link: {pdf_url}")

        # ✅ Close New Tab and Switch Back
        driver.close()
        driver.switch_to.window(all_tabs[0])

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error on button {index + 1}: {e}")
        continue

# ✅ Save Results to JSON
output_file = "vyoma_compliances.json"
with open(output_file, "w") as f:
    json.dump(pdf_links, f, indent=4)

print("✅ Scraped PDF links saved to:", output_file)

# ✅ Close Browser
driver.quit()

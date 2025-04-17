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

# ✅ Open the Vyoma Collaterals Page
url = "https://vyoma.org/collaterals/"
driver.get(url)

# ✅ Wait for Page to Load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
time.sleep(2)

# ✅ Find the **4 Correct Buttons** (Fixed XPath)
buttons = driver.find_elements(By.XPATH, "//div[contains(@class, 'et_pb_module') and contains(@class, 'et_pb_text')]//h3")

if len(buttons) != 4:
    print(f"⚠️ Expected 4 buttons, but found {len(buttons)}! Check the XPath.")
else:
    print(f"✅ Found all 4 buttons!")

links = []

# ✅ Click Each Button & Extract URL
for index, button in enumerate(buttons):
    try:
        print(f"🔹 Clicking button {index + 1}...")

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView();", button)
        time.sleep(1)

        # Click using JavaScript
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)

        # ✅ Check if a new tab opened
        all_tabs = driver.window_handles
        if len(all_tabs) > 1:
            driver.switch_to.window(all_tabs[-1])
        else:
            print(f"❌ No new tab opened for button {index + 1}. Retrying click...")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
            all_tabs = driver.window_handles
            if len(all_tabs) > 1:
                driver.switch_to.window(all_tabs[-1])
            else:
                print(f"❌ Still no new tab for button {index + 1}")
                continue

        time.sleep(2)

        # ✅ Get the URL
        link_url = driver.current_url
        print(f"✅ Extracted Link {index + 1}: {link_url}")

        # ✅ Save all links (PDF + HTML)
        links.append(link_url)

        # Close the new tab and switch back
        driver.close()
        driver.switch_to.window(all_tabs[0])

        time.sleep(2)

    except Exception as e:
        print(f"❌ Error on button {index + 1}: {e}")
        continue

# ✅ Save Results to JSON
output_file = "vyoma_collaterals.json"
with open(output_file, "w") as f:
    json.dump(links, f, indent=4)

print("✅ Scraped links saved to:", output_file)

# ✅ Close Browser
driver.quit()

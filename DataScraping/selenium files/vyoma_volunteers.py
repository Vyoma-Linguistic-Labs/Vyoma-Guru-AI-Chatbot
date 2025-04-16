import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless mode (no UI)
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(service=service, options=options)
driver.get("https://vyoma.org/volunteers/")

# Wait setup
wait = WebDriverWait(driver, 10)

# Store scraped data
volunteers_data = {
    "volunteer_of_the_month": None,
    "volunteers": {}
}

print("🚀 Scraping started...")

### **1️⃣ Scrape "Volunteer of the Month" Section** ###
try:
    print("🔍 Looking for Volunteer of the Month...")
    vol_month_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "et_pb_gallery_item")))
    name = vol_month_section.find_element(By.CLASS_NAME, "et_pb_gallery_title").text.strip()
    volunteers_data["volunteer_of_the_month"] = name
    print(f"✅ Volunteer of the Month: {name}")
except Exception as e:
    print(f"⚠️ Volunteer of the Month not found: {e}")

### **2️⃣ Scrape "All Volunteers" Categorized** ###
previous_page_source = ""  # Store page source to detect changes

while True:
    time.sleep(2)  # Allow elements to load

    # Get the current page source
    current_page_source = driver.page_source

    # If the page content hasn't changed, break the loop (prevents infinite loop)
    if current_page_source == previous_page_source:
        print("🔚 No new data found. Stopping pagination.")
        break

    previous_page_source = current_page_source  # Update for next iteration

    # Find all categories (each has an H2 heading)
    category_elements = driver.find_elements(By.CLASS_NAME, "et_pb_text_inner")

    for category_element in category_elements:
        try:
            # Extract the category name
            category_name = category_element.find_element(By.TAG_NAME, "h2").text.strip()
            if category_name not in volunteers_data["volunteers"]:
                volunteers_data["volunteers"][category_name] = []  # Initialize category

            print(f"🔍 Scraping category: {category_name}")

            # Find all volunteers *below* this category
            volunteer_elements = category_element.find_elements(By.XPATH, "./following-sibling::div//h3[@class='et_pb_gallery_title']")
            for vol in volunteer_elements:
                name = vol.text.strip()
                if name and name not in volunteers_data["volunteers"][category_name]:
                    volunteers_data["volunteers"][category_name].append(name)

            print(f"✅ Found {len(volunteer_elements)} volunteers in {category_name}")

        except Exception as e:
            print(f"⚠️ Skipping category due to error: {e}")

    # Check for "Next" button
    try:
        next_button = driver.find_element(By.CLASS_NAME, "page-next")
        if not next_button.is_displayed():  # Check if button is hidden
            print("🔚 No more pages. Stopping pagination.")
            break
        else:
            print("➡️ Clicking Next Page...")
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)  # Allow next page to load
    except Exception as e:
        print(f"⚠️ No 'Next' button found: {e}")
        break  # No next button means last page

# Close browser
driver.quit()

# Save data to JSON
with open("vyoma_volunteers.json", "w", encoding="utf-8") as f:
    json.dump(volunteers_data, f, indent=4, ensure_ascii=False)

print("✅ Scraping completed! Data saved in vyoma_volunteers.json")

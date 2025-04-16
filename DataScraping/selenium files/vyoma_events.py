import json
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define output file path in the current script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "vyoma_events.json")

def get_driver():
    """Initialize and return a Selenium WebDriver instance."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

def scrape_vyoma_events():
    """Scrape event data from Vyoma website."""
    driver, wait = get_driver()
    url = "https://vyoma.org/events/#/"
    driver.get(url)

    events_data = []

    def scrape_events():
        """Extract event details from the current page."""
        events = driver.find_elements(By.CSS_SELECTOR, "div.sv-tile.sv-list-view.sv-size-big")
        for event in events:
            try:
                name = event.find_element(By.CSS_SELECTOR, "h3.sv-tile__title").text.strip()
                date = event.find_element(By.CSS_SELECTOR, "div.sv-badge-list div.sv-badge").text.strip()
                details_link = event.find_element(By.CSS_SELECTOR, "a.sv-tile__btn").get_attribute("href")

                # Store extracted data
                events_data.append({
                    "name": name,
                    "date": date,
                    "details_link": details_link
                })
            except Exception as e:
                print(f"⚠️ Skipping an event due to error: {e}")

    # Scrape the first page
    scrape_events()

    # Handle pagination
    while True:
        try:
            next_button_parent = driver.find_element(By.CSS_SELECTOR, "li.sv-pagination__next")
            next_button = next_button_parent.find_element(By.TAG_NAME, "a")
            if next_button.is_displayed():
                print("➡️ Clicking Next Page...")
                next_button.click()
                time.sleep(3)  # Wait for new content to load

                # Ensure new events are loaded
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sv-tile.sv-list-view.sv-size-big")))
                scrape_events()
            else:
                print("✅ No more pages. Exiting loop.")
                break
        except Exception as e:
            print(f"⚠️ Pagination ended or error occurred: {e}")
            break

    # Save data as JSON in the script's directory
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"vyoma_events": events_data}, f, indent=4, ensure_ascii=False)

    driver.quit()
    print(f"\n✅ Scraping complete! Data saved in {OUTPUT_FILE}")

if __name__ == "__main__":
    scrape_vyoma_events()

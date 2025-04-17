from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import time

# Set up Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode (remove if debugging)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

# URL of the Testimonials page
url = "https://vyoma.org/testimonials/"
driver.get(url)

# Wait for testimonials to load initially
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ndrsl-live-testimonial")))

# Scroll down to load all testimonials (handle lazy loading)
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Allow testimonials to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# **Force scroll into the last testimonial**
testimonials = driver.find_elements(By.CLASS_NAME, "ndrsl-live-testimonial")
if testimonials:
    last_testimonial = testimonials[-1]  # Get the last one
    driver.execute_script("arguments[0].scrollIntoView(true);", last_testimonial)
    time.sleep(2)  # Wait for it to fully load

# Extract all testimonials after ensuring last one is visible
testimonials = driver.find_elements(By.CLASS_NAME, "ndrsl-live-testimonial")

# List to store scraped data
testimonial_data = []

# Loop through each testimonial and extract details
for index, testimonial in enumerate(testimonials, start=1):
    try:
        # Extract Name
        try:
            name = testimonial.find_element(By.CSS_SELECTOR, "h3.ndrsl-live-user-name").text.strip()
        except NoSuchElementException:
            name = "N/A"

        # Extract Company/Affiliation
        try:
            company = testimonial.find_element(By.CSS_SELECTOR, "h4.ndrsl-live-user-company").text.strip()
        except NoSuchElementException:
            company = "N/A"

        # Extract Comment
        try:
            comment = testimonial.find_element(By.CSS_SELECTOR, "p.ndrsl-live-user-comments").text.strip()
        except NoSuchElementException:
            comment = "N/A"

        # Store data in dictionary
        testimonial_data.append({
            "name": name,
            "company": company,
            "comment": comment
        })

        print(f"Extracted Testimonial {index}: {name}")

    except Exception as e:
        print(f"Error extracting testimonial {index}: {e}")

# Close the WebDriver
driver.quit()

# Double-check total number of testimonials scraped
print(f"Total testimonials scraped: {len(testimonial_data)}")

# Save data to JSON file
output_filename = "vyoma_testimonials.json"
with open(output_filename, "w", encoding="utf-8") as json_file:
    json.dump(testimonial_data, json_file, ensure_ascii=False, indent=4)

print(f"Scraping completed! Data saved to {output_filename}")

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import json
import time

class ItarashastraSpider(scrapy.Spider):
    name = "vyoma_itarashastra"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def __init__(self, *args, **kwargs):
        super(ItarashastraSpider, self).__init__(*args, **kwargs)

        # ✅ Setup Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(5)  # ✅ Ensure JavaScript has time to load

        sel = Selector(text=self.driver.page_source)

        # ✅ Locate the correct section
        table_rows = sel.xpath('//div[contains(@class, "dipl_tabs_item_4")]//table//tr')

        data = []
        current_category = None

        for row in table_rows:
            category = row.xpath('./td[1]/text()').get()
            title = row.xpath('./td[2]/a/text()').get()
            link = row.xpath('./td[2]/a/@href').get()

            if category:
                current_category = category  # ✅ Update category if present

            if title and link:
                data.append({
                    "category": current_category,
                    "title": title.strip(),
                    "link": link.strip()
                })

        # ✅ Save as JSON (in the same directory as the script)
        output_file = "vyoma_itarashastra.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.driver.quit()
        self.log(f"✅ Data saved to {output_file}")


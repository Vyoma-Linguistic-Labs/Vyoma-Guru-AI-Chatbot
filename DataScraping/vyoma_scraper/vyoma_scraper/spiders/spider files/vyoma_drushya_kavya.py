import scrapy
import json

class VyomaDrushyaKavyaSpider(scrapy.Spider):
    name = "vyoma_drushya_kavya"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        drushya_section = response.xpath('//div[contains(@class, "dipl_tabs_item_6")]')
        items = []
        last_category = None  # Store the last non-empty category

        for row in drushya_section.xpath('.//tr'):
            category = row.xpath('td[1]/text()').get()  # First column (Category)
            name = row.xpath('td[2]/a/text()').get()  # Second column (Course Name)
            url = row.xpath('td[2]/a/@href').get()  # Course Link

            if category:
                last_category = category.strip()  # Update last known category

            if name and url:
                items.append({
                    "category": last_category if last_category else "Unknown",
                    "name": name.strip(),
                    "url": url.strip()
                })

        # Save output in JSON file
        with open("drushya_kavya.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        self.log(f"Saved {len(items)} items to drushya_kavya.json")

        return items

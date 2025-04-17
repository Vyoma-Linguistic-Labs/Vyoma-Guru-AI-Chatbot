import scrapy
import json
from collections import OrderedDict

class VyomaShravyaSpider(scrapy.Spider):
    name = "vyoma_shravya"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        shravya_section = response.xpath('//div[contains(@class, "dipl_tabs_item_7")]')
        items = []
        last_category = "Shravya"  # Ensure there's always a default category

        for row in shravya_section.xpath('.//tr'):
            category = row.xpath('td[1]/text()').get()
            if category and category.strip():
                last_category = category.strip()  # Update only if a new category is found
            
            name = row.xpath('td[2]/a/text()').get()
            url = row.xpath('td[2]/a/@href').get()

            if name and url:
                items.append({
                    "category": last_category,  # Always use last known category
                    "name": name.strip(),
                    "url": url.strip()
                })

        # **REMOVE DUPLICATES BUT PRESERVE ORDER**
        unique_items = list(OrderedDict((json.dumps(item, sort_keys=True), item) for item in items).values())

        # **SAVE TO JSON**
        output_file = "vyoma_shravya.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(unique_items, f, ensure_ascii=False, indent=4)

        self.log(f"✅ Successfully saved {len(unique_items)} unique items to {output_file}")

        return unique_items  # Ensure Scrapy doesn't reprocess duplicates

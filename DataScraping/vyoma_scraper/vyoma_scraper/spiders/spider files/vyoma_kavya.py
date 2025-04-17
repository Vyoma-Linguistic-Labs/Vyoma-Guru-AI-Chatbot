import scrapy
import json

class VyomaKavyaSpider(scrapy.Spider):
    name = "vyoma_kavya"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        kavya_section = response.xpath('//div[contains(@class, "dipl_tabs_item_5")]')
        items = []

        for link in kavya_section.xpath('.//a'):
            name = link.xpath('text()').get()
            url = link.xpath('@href').get()

            if name and url:
                items.append({"category": "Kavya", "name": name.strip(), "url": url.strip()})

        # Save output in JSON file
        with open("kavya_data.json", "w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=4)

        self.log(f"Saved {len(items)} items to kavya_data.json")

        return items

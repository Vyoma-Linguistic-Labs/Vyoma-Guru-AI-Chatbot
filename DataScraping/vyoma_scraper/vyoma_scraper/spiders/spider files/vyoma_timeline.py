import scrapy
import json

class VyomaTimelineSpider(scrapy.Spider):
    name = "vyoma_timeline"
    start_urls = ["https://vyoma.org/timeline/"]

    def parse(self, response):
        timeline_items = response.xpath("//div[contains(@class, 'dipl_timeline_item')]")

        unique_entries = set()  # ✅ Set to track unique (year, title) pairs
        data = []

        for item in timeline_items:
            year = item.xpath(".//div[contains(@class, 'dipl_item_time')]/text()").get()
            title = item.xpath(".//div[contains(@class, 'dipl_item_content')]//h3/text()").get()
            description = item.xpath(".//div[contains(@class, 'dipl_item_desc')]//p/text()").getall()

            # Clean and join multi-line descriptions
            description = " ".join(desc.strip() for desc in description) if description else ""

            if year and title:
                entry_key = (year.strip(), title.strip())  # ✅ Unique key for each entry
                
                if entry_key not in unique_entries:
                    unique_entries.add(entry_key)  # ✅ Add to the set to prevent duplicates
                    data.append({
                        "year": year.strip(),
                        "title": title.strip(),
                        "description": description
                    })

        # ✅ JSON Block: Save the scraped data as a JSON file
        json_data = {"timeline": data}
        with open("vyoma_timeline.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        yield json_data  # ✅ Return the JSON data


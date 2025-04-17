import scrapy
import json

class VyomaToolsSpider(scrapy.Spider):
    name = "vyoma_tools"
    start_urls = ["https://vyoma.org/where-sanskrit/"]  # Update if needed

    def parse(self, response):
        data = {"category": "Vyoma Tools", "entries": []}

        # Find the main container for Vyoma Tools
        section = response.xpath('//div[contains(@class, "dipl_tabs_item_6")]')

        if not section:
            self.logger.error("Could not find the Vyoma Tools section.")
            return

        # Extract subcategories (bold underlined text)
        subcategories = section.xpath('.//p/strong/u/text()').getall()

        # Extract links under each subcategory
        lists = section.xpath('.//ol')

        if len(subcategories) != len(lists):
            self.logger.warning("Mismatch in subcategories and lists. Some data may be missing.")

        for index, subcategory in enumerate(subcategories):
            category_name = subcategory.strip()
            links = lists[index].xpath('.//a')

            subcategory_entries = []

            for link in links:
                title = link.xpath('text()').get()
                url = link.xpath('@href').get()

                if title and url:
                    subcategory_entries.append({"title": title.strip(), "url": response.urljoin(url)})

            if subcategory_entries:
                data["entries"].append({"subcategory": category_name, "links": subcategory_entries})

        # Save data to JSON file (optional)
        with open("vyoma_tools.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        yield data

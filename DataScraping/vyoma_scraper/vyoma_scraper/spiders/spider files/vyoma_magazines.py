import scrapy
import json

class VyomaMagazinesSpider(scrapy.Spider):
    name = "vyoma_magazines"
    start_urls = ["https://vyoma.org/where-sanskrit/"]

    def parse(self, response):
        category_name = "Magazines and Journals"
        data = {"category": category_name, "items": []}
        seen_titles = set()  # To track and prevent duplicate titles

        # Locate the correct section
        section = response.css(".dipl_tabs_item_2 .dipl_tab_desc")

        if section:
            for link in section.css("a"):
                title = link.xpath("text()").get(default="").strip()
                url = link.attrib.get("href", "").strip()

                # Ensure no duplicates and valid entries
                if title and url and title not in seen_titles:
                    data["items"].append({"title": title, "url": url})
                    seen_titles.add(title)  # Mark title as seen

        # Save data to JSON file
        filename = "vyoma_magazines.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([data], f, ensure_ascii=False, indent=4)

        self.log(f"Data saved to {filename}")

        yield data

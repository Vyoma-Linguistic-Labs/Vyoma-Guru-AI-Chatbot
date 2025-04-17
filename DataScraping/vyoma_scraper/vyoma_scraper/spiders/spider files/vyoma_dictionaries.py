import scrapy
import json

class VyomaDictionariesSpider(scrapy.Spider):
    name = "vyoma_dictionaries"
    start_urls = ["https://vyoma.org/where-sanskrit/"]

    def parse(self, response):
        # Locate the correct section
        section = response.css("div.dipl_tabs_item_4 .dipl_tab_desc")

        dictionary_links = []
        for item in section.css("li"):  # Extracting list items to get better context
            title = item.xpath("normalize-space(.)").get()  # Get the full text inside <li>
            url = item.css("a::attr(href)").get()  # Extract URL from <a> tag
            if url:
                dictionary_links.append({"title": title, "url": url})

        # Save extracted data
        data = {"category": "Vyoma Dictionaries", "entries": dictionary_links}

        # Save to JSON file
        with open("vyoma_dictionaries.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        yield data  # Output for Scrapy


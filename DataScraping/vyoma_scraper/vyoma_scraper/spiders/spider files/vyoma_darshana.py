import scrapy
import json

class VyomaDarshanaSpider(scrapy.Spider):
    name = "vyoma_darshana"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        category_name = "Darshana"
        entries = []

        rows = response.xpath("//div[contains(@class, 'dipl_tabs_item_3')]//table//tr")
        
        current_subcategory = None  # To keep track of subcategory names

        for row in rows:
            columns = row.xpath(".//td")
            if len(columns) == 2:
                subcategory = columns[0].xpath("normalize-space(text())").get()
                link_text = columns[1].xpath("normalize-space(a/text())").get()
                link_href = columns[1].xpath("a/@href").get()

                # If the first column has a name, update the subcategory tracker
                if subcategory:
                    current_subcategory = subcategory
                elif not subcategory and current_subcategory:
                    subcategory = current_subcategory  # Keep using the last valid subcategory

                if link_text and link_href:
                    entries.append({
                        "Name": subcategory if subcategory else "General",
                        "Link": link_href,
                        "Title": link_text
                    })

        # Create final structured JSON output
        output_data = [{
            "Category": category_name,
            "Entries": entries
        }]

        # Save to JSON file
        with open("darshana.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        self.log(f"Saved data to darshana.json")

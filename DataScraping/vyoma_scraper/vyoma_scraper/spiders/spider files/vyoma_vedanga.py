import scrapy
import json

class VedangaSpider(scrapy.Spider):
    name = "vedanga"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        category_name = "Vedanga"
        entries = []

        # Selecting the relevant table under the Vedanga category
        vedanga_section = response.xpath("//div[contains(@class, 'dipl_tabs_item_2')]")

        if vedanga_section:
            rows = vedanga_section.xpath(".//table/tbody/tr")
            current_subcategory = None  # To track subcategories

            for row in rows:
                columns = row.xpath("./td")
                if len(columns) == 2:
                    subcategory = columns[0].xpath("normalize-space(text())").get()
                    link = columns[1].xpath("./a/@href").get()
                    name = columns[1].xpath("normalize-space(./a/text())").get()

                    if subcategory:  # If subcategory exists, update it
                        current_subcategory = subcategory
                    elif not subcategory and current_subcategory:
                        subcategory = current_subcategory

                    if subcategory and name and link:
                        entries.append({
                            "Subcategory": subcategory,
                            "Name": name,
                            "Link": link
                        })

        result = [{"Category": category_name, "Entries": entries}]

        # Save the JSON output
        with open("vedanga.json", "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        self.log("Saved vedanga.json")

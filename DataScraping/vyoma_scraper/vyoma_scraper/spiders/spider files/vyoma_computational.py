import scrapy
import json

class VyomaComputationalSpider(scrapy.Spider):
    name = "vyoma_computational"
    start_urls = ["https://vyoma.org/where-sanskrit/"]

    def parse(self, response):
        category_name = "Computational Tools"
        table = response.xpath('//table[@id="tablepress-7"]')

        if table:
            rows = table.xpath(".//tbody/tr")
            data = [
                {
                    "Sl. No": row.xpath(".//td[1]//text()").get(default="").strip(),
                    "Website Name": row.xpath(".//td[2]//text()").get(default="").strip(),
                    "Website Link": row.xpath(".//td[3]//a/@href").get(default="").strip(),
                    "Short Description": row.xpath(".//td[4]//text()").get(default="").strip(),
                }
                for row in rows
            ]

            result = {category_name: data}

            with open("computational_tools.json", "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=4)

            self.log(f"Scraped {len(data)} items from {category_name}.")

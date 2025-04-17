import scrapy
import json

class VyomaRepositoriesSpider(scrapy.Spider):
    name = "vyoma_repositories"
    start_urls = ["https://vyoma.org/where-sanskrit/"]

    def parse(self, response):
        category_name = "Repositories of Sanskrit Texts"
        rows = response.xpath('//table[@id="tablepress-6"]//tbody/tr')

        data = [
            {
                "Sl. No": row.xpath(".//td[1]//text()").get(default="").strip(),
                "Title": row.xpath(".//td[2]//text()").get(default="").strip(),
                "Author/Source": row.xpath(".//td[3]//text()").get(default="").strip(),
                "Website Link": row.xpath(".//td[4]//a/@href").get(default="").strip(),
                "Short Description": row.xpath(".//td[5]//text()").get(default="").strip(),
            }
            for row in rows
        ]

        result = {category_name: data}

        with open("vyoma_repositories.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

        self.log(f"Scraped {len(data)} items from {category_name}.")

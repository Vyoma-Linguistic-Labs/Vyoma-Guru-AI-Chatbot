import scrapy
import json

class VyomaELearningSpider(scrapy.Spider):
    name = "vyoma_elearning"
    start_urls = ["https://vyoma.org/where-sanskrit/"]  # Update if needed

    def parse(self, response):
        section = response.xpath("//div[contains(@class, 'dipl_tabs_item_7')]")  # Target Vyoma eLearning
        links = section.xpath(".//a")

        data = []
        for link in links:
            # Extract text from the link and its child elements
            name = link.xpath(".//text()").getall()
            name = " ".join([text.strip() for text in name if text.strip()]).strip()  # Join multiple text parts
            url = link.xpath("@href").get()

            if name and url:
                data.append({"name": name, "url": url})

        # Save data to JSON file
        with open("vyoma_elearning.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.log(f"Scraped {len(data)} links from Vyoma eLearning.")


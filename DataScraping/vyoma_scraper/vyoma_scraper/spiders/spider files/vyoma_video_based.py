import scrapy
import json

class VyomaVideoBasedSpider(scrapy.Spider):
    name = "vyoma_video_based"
    start_urls = ["https://vyoma.org/where-sanskrit/"]

    def parse(self, response):
        category_name = "Vyoma Video-Based Learning"
        data = []

        for item in response.css("div.et_pb_module.dipl_tabs_item_1 li"):
            name = item.css("::text").get()
            url = item.css("a::attr(href)").get()

            if name and url:
                data.append({
                    "category": category_name,
                    "name": name.strip(),
                    "url": url.strip(),
                })

        # Save data to a JSON file
        with open("vyoma_video_based.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # Print extracted data
        print(json.dumps(data, ensure_ascii=False, indent=4))

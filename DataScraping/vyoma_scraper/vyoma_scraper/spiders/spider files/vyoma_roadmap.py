import scrapy
import json

class VyomaRoadmapSpider(scrapy.Spider):
    name = "vyoma_roadmap"
    start_urls = ["https://vyoma.org/roadmap/"]

    def parse(self, response):
        roadmap_items = []
        seen_titles = set()  # To avoid duplicates

        for item in response.xpath("//div[contains(@class, 'dipl_timeline_item')]"):
            title = item.xpath(".//h3/text()").get(default="").strip()
            description = item.xpath(".//div[contains(@class, 'dipl_item_desc')]/p/text()").getall()
            description = " ".join(desc.strip() for desc in description if desc.strip())

            # Avoid duplicate entries
            if title and title not in seen_titles:
                seen_titles.add(title)
                roadmap_items.append({
                    "title": title,
                    "description": description
                })

        # Save as JSON
        with open("vyoma_roadmap.json", "w", encoding="utf-8") as f:
            json.dump({"roadmap": roadmap_items}, f, ensure_ascii=False, indent=4)

        self.log(f"Saved {len(roadmap_items)} unique roadmap items to vyoma_roadmap.json")

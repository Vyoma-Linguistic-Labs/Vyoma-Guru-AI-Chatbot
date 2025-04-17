import scrapy
import json

class VideoBasedLearningSpider(scrapy.Spider):
    name = "video_based_learning"
    start_urls = ["https://vyoma.org/"]

    def parse(self, response):
        data = {
            "Category": "Video-Based Learning",
            "Entries": []
        }

        # Targeting the specific div for "Video-Based Learning"
        video_section = response.xpath('//div[contains(@class, "dipl_tabs_item_1") and contains(@class, "dipl_active_tab_content")]')

        if video_section:
            entries = video_section.xpath('.//ol/li')  # Extract all list items within the section

            for entry in entries:
                name = entry.xpath('.//text()').get(default="").strip()
                link = entry.xpath('.//a/@href').get(default="").strip()

                # Ensuring only valid entries are added
                if name and link:
                    data["Entries"].append({"Name": name, "Link": link})

        # Save output as JSON
        with open("video_based_learning.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.log("✅ Scraping completed successfully!")

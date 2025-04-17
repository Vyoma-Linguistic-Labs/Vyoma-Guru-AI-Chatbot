import scrapy
import json

class VyomaUpavedaSpider(scrapy.Spider):
    name = "vyoma_upaveda"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        upaveda_data = {
            "Category": "Upaveda",
            "Entries": []
        }

        # Find all sections, then locate Upaveda based on its position
        sections = response.css("div.dipl_tabs_item")
        
        if len(sections) > 1:  # Ensure Upaveda section exists
            upaveda_section = sections[1]  # Second tab (index 1) is Upaveda

            for item in upaveda_section.css("div.dipl_tab_desc p"):
                name = item.css("a::text").get()
                link = item.css("a::attr(href)").get()

                if name and link:
                    upaveda_data["Entries"].append({
                        "Name": name.strip(),
                        "Link": link.strip()
                    })

        # Save to JSON file (formatted output)
        with open("upaveda.json", "w", encoding="utf-8") as f:
            json.dump(upaveda_data, f, ensure_ascii=False, indent=4)

        self.log("Data saved to upaveda.json")

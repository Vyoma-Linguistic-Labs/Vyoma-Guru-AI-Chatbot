import scrapy
import json

class VyomaLeadershipSpider(scrapy.Spider):
    name = "vyoma_leadership"
    start_urls = ["https://vyoma.org/leadership/"]

    def parse(self, response):
        leaders = set()  # Using a set to prevent duplicates

        for leader in response.xpath("//div[contains(@class, 'et_pb_team_member')]"):
            name = leader.xpath(".//h4/text()").get()
            position = leader.xpath(".//p/text()").get()

            if name and position:
                leader_tuple = (name.strip(), position.strip())  # Store as tuple to check uniqueness
                leaders.add(leader_tuple)

        # Convert set back to a list of dictionaries
        unique_leaders = [{"name": name, "position": position} for name, position in leaders]

        # Save data to JSON file
        data = {"leadership": unique_leaders}
        with open("vyoma_leadership.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        yield data  # Yielding data for Scrapy output

import scrapy
import json

class VyomaTeamSpider(scrapy.Spider):
    name = "vyoma_associates"
    start_urls = ["https://vyoma.org/team/"]

    def parse(self, response):
        team_data = []
        teams = response.xpath("//div[contains(@class, 'et_pb_team_member_description')]")

        for team in teams:
            name = team.xpath(".//h4/text()").get()
            position = team.xpath(".//p/text()").get()

            if name and position:
                team_data.append({"name": name.strip(), "position": position.strip()})

        # Remove duplicates
        unique_teams = {json.dumps(d, sort_keys=True): d for d in team_data}.values()

        # Save as JSON
        with open("vyoma_associates.json", "w", encoding="utf-8") as f:
            json.dump(list(unique_teams), f, indent=4, ensure_ascii=False)

        self.log("Saved vyoma_associates.json")
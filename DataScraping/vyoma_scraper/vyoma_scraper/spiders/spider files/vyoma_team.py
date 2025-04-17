import scrapy
import json

class VyomaTeamSpider(scrapy.Spider):
    name = "vyoma_team"
    start_urls = ["https://vyoma.org/team/"]

    def parse(self, response):
        teams_data = []

        # Extract all team sections
        team_sections = response.xpath("//div[contains(@class, 'et_pb_section')]")

        for section in team_sections:
            team_name = section.xpath(".//h2/text()").get()

            if team_name:
                members = []
                # Find all members inside this section
                member_blocks = section.xpath(".//div[contains(@class, 'et_pb_team_member_description')]")

                for member in member_blocks:
                    name = member.xpath(".//h4/text()").get()
                    position = member.xpath(".//p/text()").get()

                    if name:
                        members.append({
                            "name": name.strip(),
                            "position": position.strip() if position else "N/A"
                        })

                if members:
                    teams_data.append({"team": team_name.strip(), "members": members})

        # Save data in JSON format
        with open("vyoma_team.json", "w", encoding="utf-8") as f:
            json.dump(teams_data, f, indent=4, ensure_ascii=False)

        self.log("Saved vyoma_team.json")
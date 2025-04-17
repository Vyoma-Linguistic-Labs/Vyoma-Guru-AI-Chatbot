import scrapy
import json


class VyomaAboutSpider(scrapy.Spider):
    name = "vyoma_about"
    start_urls = ["https://vyoma.org/about/"]

    def parse(self, response):
        # Select only the main content section, avoiding navbars and footers
        main_content = response.xpath("//div[contains(@class, 'et_pb_section') and not(contains(@class, 'footer'))]")

        content = []

        # Extract all paragraphs, lists, and blurbs
        for block in main_content.xpath(".//div[contains(@class, 'et_pb_text_inner') or contains(@class, 'et_pb_blurb_description')]"):
            # Extract text content inside the block (includes paragraphs and list items)
            text = block.xpath(".//p//text() | .//li//text()").getall()
            text = " ".join([t.strip() for t in text if t.strip()])  # Join and clean text
            if text:
                content.append(text)

        # Extract links embedded in the content
        links = []
        for link in main_content.xpath(".//a"):
            url = link.xpath("@href").get()
            anchor_text = link.xpath("normalize-space(.)").get()
            if url and anchor_text:
                links.append({"text": anchor_text, "url": url})

        # Save everything in a JSON file
        data = {
            "page": "About Vyoma",
            "content": content,  # Every para, list, and blurb is stored here
            "links": links,  # All embedded links
        }

        with open("vyoma_about.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        self.log("Saved data to vyoma_about.json")

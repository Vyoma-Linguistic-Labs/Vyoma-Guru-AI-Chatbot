import scrapy
import json

class VyomaNewsletterSpider(scrapy.Spider):
    name = "vyoma_newsletter"
    start_urls = ["https://vyoma.org/new-letter/"]

    def parse(self, response):
        pdf_links = response.xpath("//iframe/@src").extract()

        # Ensure full URLs (some might be relative)
        pdf_links = [response.urljoin(link) for link in pdf_links]

        # ✅ Save to JSON
        output_file = "vyoma_newsletter.json"
        with open(output_file, "w") as f:
            json.dump(pdf_links, f, indent=4)

        self.log(f"✅ Scraped {len(pdf_links)} PDF links and saved to {output_file}")

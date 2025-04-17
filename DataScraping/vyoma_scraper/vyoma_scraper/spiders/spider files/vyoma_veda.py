import scrapy


class VyomaVedaSpider(scrapy.Spider):
    name = "vyoma_veda"
    start_urls = ["https://vyoma.org/what-sanskrit/"]

    def parse(self, response):
        # Locate the Veda category's section
        veda_section = response.css("div.dipl_tabs_item_0.dipl_active_tab_content")

        entries = []
        for item in veda_section.css("div.dipl_tab_desc p"):
            name = item.xpath("normalize-space(text())").get("")
            link = item.css("a::attr(href)").get(default="").strip()
            link_text = item.css("a::text").get(default="").strip()

            # Clean up the text and remove unwanted colons
            if name.endswith(":"):
                name = name[:-1].strip()

            # Use the link text if available
            if link and link_text:
                name = link_text  

            if name and link:
                entries.append({"Name": name, "Link": link})

        yield {
            "Category": "Veda",
            "Entries": entries,
        }

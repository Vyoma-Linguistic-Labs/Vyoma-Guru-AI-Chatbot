import scrapy
import json

class VyomaBlogsSpider(scrapy.Spider):
    name = "vyoma_orgblogs"
    start_urls = ["https://vyoma.org/blogs/"]
    scraped_blogs = []  # ✅ Store blogs in memory to avoid duplication

    def parse(self, response):
        articles = response.xpath("//article[contains(@class, 'blog_post')]")

        for article in articles:
            title = article.xpath(".//h2[@class='entry-title']/a/text()").get()
            date = article.xpath(".//span[@class='published']/text()").get()
            description = article.xpath(".//div[@class='post-content-inner']/p/text()").get()
            read_more_link = article.xpath(".//a[contains(@class, 'more-link')]/@href").get()

            if title and read_more_link:
                blog_data = {
                    "title": title.strip() if title else "N/A",
                    "date": date.strip() if date else "N/A",
                    "description": description.strip() if description else "N/A",
                    "read_more_link": response.urljoin(read_more_link)
                }

                # ✅ Avoid duplicates by checking if it's already scraped
                if blog_data not in self.scraped_blogs:
                    self.scraped_blogs.append(blog_data)

        # ✅ Check for "Older Entries" button to go to the next page
        next_page = response.xpath("//a[contains(text(), 'Older Entries')]/@href").get()

        if next_page:
            self.log(f"🔄 Found next page: {next_page}")
            yield response.follow(next_page, callback=self.parse)
        else:
            self.log("🚀 No more pages found. Writing to file...")

            # ✅ Write all collected data to JSON once at the end
            output_file = "vyoma_orgblogs.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(self.scraped_blogs, f, indent=4, ensure_ascii=False)
            
            self.log(f"✅ Scraped {len(self.scraped_blogs)} blogs saved to {output_file}")

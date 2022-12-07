import scrapy
import re
from scrapy_selenium import SeleniumRequest
import pandas as pd

from .pdf import getFBPDFContent

contentLst = list()


class MetaSpider(scrapy.Spider):
    name = 'FBCrawler'

    def start_requests(self):
        urls = ["https://investor.fb.com/investor-events/default.aspx"]

        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = f"content-{page}.html"

        # with open(filename, "wb") as f:
        #     f.write(response.body)
        #     self.log(f"Saved file {filename}")

        container = response.xpath(
            '//*[@id="_ctrl0_ctl54_divModuleContainer"]/div[1]/div').css(".ModuleItemRow")

        for item in container:
            title = item.css('.ModuleHeadlineLink').xpath('text()').get()

            if "Earnings" not in title:
                continue

            title = re.sub(r'\s+', ' ', title)
            pdf = item.css(
                '.RelatedDocuments div:first-child a::attr(href)').get()
            print(f"pdf : {pdf}")
            content = getFBPDFContent(pdf)

            print(f"{title:<20} : {content}")

            contentLst.append(
                {'quarter': title, 'DAP': content[0], 'MAP': content[1], 'DAU': content[2], 'MAU': content[3]})

        contents = pd.DataFrame.from_records(
            contentLst, columns=['quarter', 'DAP', 'MAP', 'DAU', 'MAU'])
        contents.to_csv("FB.csv", index=False)

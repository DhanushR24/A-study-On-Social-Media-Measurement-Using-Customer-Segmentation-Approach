import scrapy
import re
from scrapy_selenium import SeleniumRequest
import pandas as pd

from .pdf import getTwPDFContent

contentLst = list()


class MetaSpider(scrapy.Spider):
    name = 'TwCrawler'

    def start_requests(self):
        urls = [
            "https://investor.twitterinc.com/financial-information/quarterly-results/default.aspx"]

        for url in urls:
            yield SeleniumRequest(
                url=url,
                wait_time=3,
                screenshot=True,
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):

        container = response.xpath(
            '//*[@id="_ctrl0_ctl48_divModuleContainer"]/div/div/div/div[2]')
        print("Parsed content sdsd: ", container)

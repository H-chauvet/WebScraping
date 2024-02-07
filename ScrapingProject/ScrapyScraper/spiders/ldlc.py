"""
List of imports
"""
import json
from http.client import HTTPResponse
from bs4 import BeautifulSoup

import scrapy
from scrapy import Request
from scrapy.http.response.html import HtmlResponse

from Scraping.models import Category, Website

from ScrapyScraper.items import CategoryItem, ProductItem

class LdlcSpider(scrapy.Spider):
    name = "ldlc"
    allowed_domains = ["www.ldlc.com"]
    start_urls = ["https://www.ldlc.com"]

    def parse(self, response):
        pass

"""
List of imports
"""
import os
import scrapy
from ScrapyScraper.items import WebsiteItem
from scrapy.http.response.html import HtmlResponse


class CustomSpider(scrapy.Spider):
    """CustomSpider class

    Args:
        scrapy (_type_): _description_

    Raises:
        ValueError: Error raised if website_url not defined
        ValueError: Error raised if default_start_callback not defined
    """

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        # Name existence checked by scrapy.Spider

        if not getattr(self, "website_url", None):
            raise ValueError(f"{type(self).__name__} must have a website_url")

        if not getattr(self, "default_start_callback", None):
            raise ValueError(
                f"{type(self).__name__} must have a default_start_callback"
            )

    def parse(self, response: HtmlResponse, **kwargs):
        """
        Parse site
        """
        # Create a website in database
        site_item = WebsiteItem()
        site_item["name"] = self.name
        site_item["url"] = self.website_url
        yield site_item

        # Begin scrapping (generally by main categories)
        yield from getattr(self, "default_start_callback")(response, site_item.instance)

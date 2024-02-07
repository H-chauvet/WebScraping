# Scrapy settings for example project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os
import uuid

from scrapy.crawler import install_reactor

BOT_NAME = "ScrapyScraper"

SPIDER_MODULES = ["ScrapyScraper.spiders"]
NEWSPIDER_MODULE = "ScrapyScraper.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Chrome/112.0.0.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
COOKIES_ENABLED = True


# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scraper.pipelines.WebsitePipeline": 300,
    "scraper.pipelines.CategoryPipeline": 400,
    "scraper.pipelines.ProductPipeline": 500,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True


# Default feed export settings
# See https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-export-encoding
FEED_EXPORT_ENCODING = "utf-8"

# Id to identify job
JOB_ID = os.environ.get("JOB", uuid.uuid4().hex)


# Log variables
LOG_LEVEL = "INFO"
LOG_DATEFORMAT = "%Y-%m-%dT%H:%M:%S%z"
LOG_FORMAT = (
    '{"timestamp":%(asctime)s, "job_id":'
    + JOB_ID
    + ', "logger":"%(name)s", "level":"%(levelname)s", "event":"%(message)s"}'
)

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

install_reactor(TWISTED_REACTOR)

# Django configuration
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from django.core.management.base import BaseCommand
from ScrapyScraper.spiders.ldlc import LdlcSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Release spiders"

    SPIDERS = {
        LdlcSpider.name: LdlcSpider,
    }

    def add_arguments(self, parser):
        parser.add_argument("spider_name", choices=self.SPIDERS.keys())

    def handle(self, *args, **options):
        spider = self.SPIDERS[options["spider_name"]]

        process = CrawlerProcess(get_project_settings())
        configure_logging(install_root_handler=False)

        process.crawl(spider)
        process.start()

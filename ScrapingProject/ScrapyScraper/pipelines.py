import logging

from Scraping.models import Category, Product, Website, ScraperRun
# from Scraping.utils import common
from django.utils import timezone
from ScrapyScraper.items import CategoryItem, ProductItem, WebsiteItem
from ScrapyScraper.spiders.spider_base import CustomSpider
from scrapy.utils.log import configure_logging

LOGGER = logging.getLogger("naoscrap")


class NaoScrapMixin:
    OBJECT_SCRAP = None

    def open_spider(self, _: CustomSpider):
        LOGGER.info("Begin scraping of %s", self.OBJECT_SCRAP)

    def close_spider(self, _: CustomSpider):
        LOGGER.info("Scraping of %s finished", self.OBJECT_SCRAP)


class WebsitePipeline(NaoScrapMixin):
    OBJECT_SCRAP = "Website"

    def process_item(self, item: WebsiteItem, _: CustomSpider):
        if not isinstance(item, WebsiteItem):
            return item

        try:
            website = Website.objects.get(url=item["url"])
        except Website.DoesNotExist:
            pass
        else:
            # Already exists, just update it
            instance = item.save(commit=False)
            instance.pk = website.pk

        item.save()
        return item


class CategoryPipeline(NaoScrapMixin):
    OBJECT_SCRAP = "Category"

    def process_item(self, item: CategoryItem, _: CustomSpider):
        if not isinstance(item, CategoryItem):
            return item

        try:
            category = Category.objects.get(url=item["url"])
        except Category.DoesNotExist:
            pass
        else:
            # Already exists, just update it
            instance = item.save(commit=False)
            instance.pk = category.pk

        item.save()
        return item


class ProductPipeline(NaoScrapMixin):
    OBJECT_SCRAP = "Product"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.site = None
        self.created_product_count = 0
        self.updated_product_count = 0
        self.total_product_count = 0

    def process_item(self, item: ProductItem, _: CustomSpider):
        # Get current website
        if isinstance(item, WebsiteItem):
            if not self.site:
                self.site = Website.objects.get(url=item["url"])
            elif self.site.url != item["url"]:
                raise RuntimeError(
                    "Pipeline does not support multiple websites per run"
                )

        # Ignore others objects
        if not isinstance(item, ProductItem):
            return item

        # Create or update product
        try:
            # A site could have the same code supplier (specially if the code is number) for multiples product
            # so we need another discriminator.
            # We use the category to discriminate products.
            product = Product.objects.get(
                category=item["category"], code_supplier=item["code_supplier"]
            )
        except Product.DoesNotExist:
            self.created_product_count += 1
        else:
            # Already exists, just update it
            instance = item.save(commit=False)
            instance.pk = product.pk

            if item.has_changed(product):
                instance.last_update = timezone.now()
                self.updated_product_count += 1

        product = item.save()
        self.total_product_count += 1

        # Add variants of products
        variants_data = getattr(item, "_variants", [])
        list_urls = [variant_data["url"] for variant_data in variants_data]
        variants = Product.objects.filter(product_page_url__in=list_urls)
        product.variants.add(*variants)

        # Add complementaries of products
        complementaries_data = getattr(item, "_complementaries", [])
        list_urls = [
            complementary_data["url"] for complementary_data in complementaries_data
        ]
        complementaries = Product.objects.filter(product_page_url__in=list_urls)
        product.complementaries.add(*complementaries)

        # Add alternatifs of products
        alternatifs_data = getattr(item, "_alternatifs", [])
        list_urls = [alternatif_data["url"] for alternatif_data in alternatifs_data]
        alternatifs = Product.objects.filter(product_page_url__in=list_urls)
        product.alternatifs.add(*alternatifs)

        return item

    def close_spider(self, spider):
        super().close_spider(spider)

        LOGGER.info("Product created : %s", self.created_product_count)
        LOGGER.info("Product updated : %s", self.updated_product_count)
        LOGGER.info("Product processed : %s", self.total_product_count)

        if self.site:
            ScraperRun.objects.create(
                website=self.site,
                products_created=self.created_product_count,
                products_updated=self.updated_product_count,
                products_count=self.total_product_count,
                update_time=timezone.now(),
            )

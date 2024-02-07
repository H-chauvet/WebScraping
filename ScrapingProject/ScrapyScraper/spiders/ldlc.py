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
from ScrapyScraper import utils
from ScrapyScraper.spiders.spider_base import CustomSpider

class LdlcSpider(CustomSpider):
    name = "ldlc"
    allowed_domains = ["www.ldlc.com"]
    website_url = "https://www.ldlc.com"
    start_urls = [website_url]
    
    # Some categories are not products but services
    service_categories = [
        "https://www.ldlc.com/n5351/tech-it-easy/",
        "https://www.ldlc.com/jeux-loisirs/cint3067/",
    ]
    

    def parse_categories(self, response: HtmlResponse, site: Website):
        """
        Parse each main category of site
        """
        # We get the attributes of the categories (name, url, associated website)
        selector = response.xpath("//*[@data-submenu-id]/a")
        for category in selector:
            href = category.attrib["href"]
            name = category.css("a::text").get().strip()

            if href in self.service_categories:
                continue

            # Init category item
            category_item = CategoryItem()
            category_item["name"] = name
            category_item["url"] = href
            category_item["website"] = site
            yield category_item

            # We go into the sub categories
            yield response.follow(
                href,
                callback=self.parse_sub_categories,
                cb_kwargs={"site": site, "parent_category": category_item.instance},
            )

    default_start_callback = parse_categories

    def parse_sub_categories(
        self, response: HtmlResponse, site: Website, parent_category: Category
    ):
        """
        Parse each sub category of site
        """
        # Here, we get the sub categories
        selector = response.xpath('//*[@class="list-cat"]/li/a')
        if selector:
            for sub_cat in selector:
                href = self.website_url + sub_cat.attrib["href"]
                name = sub_cat.css("h2 > em::text").get().strip()

                # Init category item
                category_item = CategoryItem()
                category_item["name"] = name
                category_item["url"] = href
                category_item["website"] = site
                category_item["parent"] = parent_category
                yield category_item

                # Go to sub-category
                yield response.follow(
                    href,
                    callback=self.parse_sub_categories,
                    cb_kwargs={"site": site, "parent_category": category_item.instance},
                )

        else:
            yield from self.parse_product_list(response, parent_category)

    def parse_product_list(self, response: HtmlResponse, category: Category):
        """
        Parse page product list
        """
        # From here, we get the products
        selector = response.xpath(
            '//*[@class="pdt-item"]/*[@class="pic"]/a/@href'
        ).extract()
        for href in selector:
            product_url = self.website_url + href
            yield response.follow(
                product_url,
                callback=self.parse_product,
                dont_filter=True,
                cb_kwargs={"category": category},
            )

        # Pass to next page
        next_page_partial_url = response.xpath(
            '//li[@class="next"]/a/@href'
        ).extract_first()
        if next_page_partial_url:
            next_page_url = self.website_url + next_page_partial_url
            yield Request(
                next_page_url,
                callback=self.parse_product_list,
                cb_kwargs={"category": category},
            )

    def parse_product(self, response: HTTPResponse, category: Category):
        """
        Parse product page
        """
        # Get main div
        product_informations = response.css(".product-detail")
        if not product_informations:
            return
        product_informations = product_informations[0]

        # Extract script
        script_tags = BeautifulSoup(
            response.xpath("//script[@type='application/ld+json']").get(),
            "html.parser",
        ).string
        data = json.loads(script_tags) if script_tags else {}

        # Extract few information
        name = data.get("name")
        product_page_url = response.url
        # Supplier
        code_supplier = product_informations.attrib["data-product-id"]

        # Description
        main_description = data.get("description")
        if not main_description:
            main_description = utils.extract_text_from_html(
                product_informations.xpath(
                    "//div[@id='description' and @class='description']"
                )
            )

        # Extract price and currency
        incl_tax_price = float(data["offers"]["price"])
        currency = data["offers"]["priceCurrency"]
        if currency == "EUR":
            currency = "€"

        ecotaxes = float(0)
        text_ecotaxes = utils.extract_text_from_html(
            product_informations.xpath('//aside/*[@class="eco"]')
        )
        if text_ecotaxes:
            ecotaxes = float(
                text_ecotaxes.replace("Éco-part. : ", "").replace("€", ".")
            )

        # Extract minimum quantity
        min_quantity = None
        selector_quantity = response.css(".quantity > input")
        if selector_quantity:
            min_quantity = int(selector_quantity.attrib["value"])

        # Extract others informations
        saler_reference = data["sku"]
        constructor_reference = data.get("mpn", "")
        brand = data["brand"]["name"]

        # Extract pictures
        pictures_data = []
        images = data.get("image", [])
        if images and not isinstance(images, list):
            images = [images]
        if not images:
            images = []
        for image_url in images:
            pictures_data.append(
                {
                    "url": image_url,
                }
            )

        # Extract variants
        variants_data = []
        variants_url = product_informations.xpath(
            '//div[@class="bloc-variants"]/*/ul/li[@data-url-id]'
        )
        for variant_url in variants_url:
            variants_data.append(
                {
                    "url": f"{self.website_url}/fiche/{variant_url.attrib['data-url-id']}.html",
                }
            )

        # Extract complementaries
        complementaries_data = []
        complementaries_url = product_informations.xpath(
            '//div[text()="Produits associés"]/following-sibling::div//a'
        )
        for complementary_url in complementaries_url:
            complementaries_data.append(
                {
                    "url": f"{self.website_url}{complementary_url.attrib['href']}",
                }
            )

        # Extract alternatifs
        alternatifs_data = []
        alternatifs_url = product_informations.xpath(
            '//div[text()="Produits similaires"]/following-sibling::div//div[contains(@class,"swiper-slide") \
            and not(contains(@class,"swiper-slide-duplicate"))]/a'
        )
        for alternatif_url in alternatifs_url:
            alternatifs_data.append(
                {
                    "url": f"{self.website_url}{alternatif_url.attrib['href']}",
                }
            )

        # Construct product
        item = ProductItem(
            name=name,
            product_page_url=product_page_url,
            category=category,
            code_supplier=code_supplier,
            main_description=main_description,
            currency=currency,
            incl_tax_price=incl_tax_price,
            ecotaxes=ecotaxes,
            min_quantity=min_quantity,
            saler_reference=saler_reference,
            constructor_reference=constructor_reference,
            brand=brand,
        )
        item._photos = pictures_data
        item._variants = variants_data
        item._complementaries = complementaries_data
        item._alternatifs = alternatifs_data

        yield item



# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from Scraping.models import Category, Product, Website
from scrapy_djangoitem import DjangoItem

class ProductItem(DjangoItem):
    django_model = Product
    fields_to_compare = [
        "name",
        "category",
        "code_supplier",
        "main_description",
        "secondary_description",
        "excl_tax_price",
        "incl_tax_price",
        "ecotaxes",
        "delivery_time",
        "min_quantity",
        "saler_reference",
        "constructor_reference",
        "brand",
        "package_in",
        "barcode_type",
        "bonus_info",
        "photos",
        "plans",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._photos = []
        self._plans = []
        self._variants = []
        self._complementaries = []
        self._alternatifs = []

    def has_changed(self, existing_instance):
        for field_name in self.fields_to_compare:
            # Skip missing field in new data
            if field_name not in self._values:
                continue

            # Extract values
            new_value = self._values[field_name]
            old_value = getattr(existing_instance, field_name)

            # Many To Many field
            if isinstance(new_value, list):
                raise NotImplementedError("Handling of list values not implemented.")

            # If there are at least one change, exit function
            if new_value != old_value:
                return True

        return False


class CategoryItem(DjangoItem):
    django_model = Category


class WebsiteItem(DjangoItem):
    django_model = Website

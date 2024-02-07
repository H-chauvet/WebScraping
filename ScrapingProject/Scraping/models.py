"""List of imports"""

from django.db import models
from tree_queries.models import TreeNode
from django.core.validators import URLValidator

class Website(models.Model):
    name = models.CharField(max_length=256, verbose_name="supplier")
    url = models.CharField(max_length=256)

    def __str__(self):
        return self.name

class Category(TreeNode):
    name = models.CharField(max_length=256, verbose_name="name")
    url = models.CharField(max_length=256)
    website = models.ForeignKey(Website, on_delete=models.SET_NULL, null=True)
    naofix_category_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class ScraperRun(models.Model):
    website = models.ForeignKey(
        Website, on_delete=models.CASCADE, related_name="scraper_runs"
    )
    update_time = models.DateTimeField(null=True, blank=True)
    products_count = models.IntegerField(default=0)
    products_created = models.IntegerField(default=0)
    products_updated = models.IntegerField(default=0)

class Product(models.Model):
    # Name of product
    name = models.CharField(max_length=200)
    # Link to product
    product_page_url = models.TextField(
        validators=[URLValidator()], default="", blank=True
    )
    # Category of product, defined by seller
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )

    # Code used by seller to identificate product
    # Some site does not have a field ID and used a complete name
    code_supplier = models.CharField(max_length=256)

    # Description of products
    main_description = models.TextField(default="", blank=True)
    secondary_description = models.TextField(default="", blank=True)

    # Currenty, Price, Taxes
    currency = models.CharField(max_length=5, default="", blank=True)
    excl_tax_price = models.FloatField(default=None, null=True, blank=True)
    incl_tax_price = models.FloatField(default=None, null=True, blank=True)
    vat = models.FloatField(default=None, null=True, blank=True, max_length=20)
    ecotaxes = models.FloatField(default=None, null=True, blank=True)

    # Time to get a product (Generally one week)
    delivery_time = models.CharField(max_length=50, default="", blank=True)

    # Min quantity (Generally 1)
    min_quantity = models.IntegerField(default=None, null=True, blank=True)

    # UGS / SKU
    saler_reference = models.CharField(max_length=20, default="", blank=True)
    # RPF / MPN
    constructor_reference = models.CharField(max_length=20, default="", blank=True)

    saler = models.CharField(max_length=100, default="", null=True, blank=True)
    package_in = models.CharField(max_length=20, default="", blank=True)
    brand = models.CharField(max_length=50, default="", null=True, blank=True)

    # Type of barcode
    barcode_type = models.CharField(max_length=30, default="", null=True, blank=True)

    # Other infos useful but too specific to a product/saler
    bonus_info = models.TextField(default="", blank=True)

    # Products who share the same core functionnalities but with few differences (color, dimension, etc ...)
    variants = models.ManyToManyField("self", blank=True)
    # Products who are useful/necessary for this product (Example : Ink for printer, alimentation cable/mouse for computer, etc ...)
    complementaries = models.ManyToManyField("self", blank=True)
    # Products who can replace this product (Example : Another laser printer from another brand)
    alternatifs = models.ManyToManyField("self", blank=True)

    # Internal value to see if its has been updated or not
    last_update = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            # For Human Search
            models.Index(fields=["name"]),
            # For Internal Search
            models.Index(
                fields=["category", "code_supplier"]
            ),  # Used to update a single product
            models.Index(
                fields=["product_page_url"]
            ),  # Used to link product between them
        ]

    def __str__(self):
        return str(self.name)


# Generated by Django 5.0.2 on 2024-02-07 16:19

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Scraping", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="name")),
                ("url", models.CharField(max_length=256)),
                (
                    "naofix_category_id",
                    models.PositiveIntegerField(blank=True, null=True),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="Scraping.category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={
                "verbose_name": "Category",
                "verbose_name_plural": "Categories",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "product_page_url",
                    models.TextField(
                        blank=True,
                        default="",
                        validators=[django.core.validators.URLValidator()],
                    ),
                ),
                ("code_supplier", models.CharField(max_length=256)),
                ("main_description", models.TextField(blank=True, default="")),
                ("secondary_description", models.TextField(blank=True, default="")),
                ("currency", models.CharField(blank=True, default="", max_length=5)),
                (
                    "excl_tax_price",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "incl_tax_price",
                    models.FloatField(blank=True, default=None, null=True),
                ),
                (
                    "vat",
                    models.FloatField(
                        blank=True, default=None, max_length=20, null=True
                    ),
                ),
                ("ecotaxes", models.FloatField(blank=True, default=None, null=True)),
                (
                    "delivery_time",
                    models.CharField(blank=True, default="", max_length=50),
                ),
                (
                    "min_quantity",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "saler_reference",
                    models.CharField(blank=True, default="", max_length=20),
                ),
                (
                    "constructor_reference",
                    models.CharField(blank=True, default="", max_length=20),
                ),
                (
                    "saler",
                    models.CharField(blank=True, default="", max_length=100, null=True),
                ),
                ("package_in", models.CharField(blank=True, default="", max_length=20)),
                (
                    "brand",
                    models.CharField(blank=True, default="", max_length=50, null=True),
                ),
                (
                    "barcode_type",
                    models.CharField(blank=True, default="", max_length=30, null=True),
                ),
                ("bonus_info", models.TextField(blank=True, default="")),
                ("last_update", models.DateTimeField(blank=True, null=True)),
                (
                    "alternatifs",
                    models.ManyToManyField(blank=True, to="Scraping.product"),
                ),
                (
                    "category",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="products",
                        to="Scraping.category",
                    ),
                ),
                (
                    "complementaries",
                    models.ManyToManyField(blank=True, to="Scraping.product"),
                ),
                ("variants", models.ManyToManyField(blank=True, to="Scraping.product")),
            ],
        ),
        migrations.CreateModel(
            name="Website",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=256, verbose_name="supplier")),
                ("url", models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name="Article",
        ),
        migrations.AddField(
            model_name="category",
            name="website",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="Scraping.website",
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["name"], name="Scraping_pr_name_23f75d_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["category", "code_supplier"],
                name="Scraping_pr_categor_b9f174_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["product_page_url"], name="Scraping_pr_product_926224_idx"
            ),
        ),
    ]

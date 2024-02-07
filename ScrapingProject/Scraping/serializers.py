from rest_framework import serializers
from .models import Product, Website, Category
from django.contrib import admin



class ProductAdmin(admin.ModelAdmin):
    """
    Serializer for product view

    Args:
        ModelSerializer (Class): Basic serializer model
    """

    class Meta:
        """
        Meta for ProductSerializer class
        """

        model = Product
        fields = "__all__"

class CategoryAdmin(admin.ModelAdmin):
    """
    Serializer for product view

    Args:
        ModelSerializer (Class): Basic serializer model
    """

    class Meta:
        """
        Meta for ProductSerializer class
        """

        model = Category
        fields = "__all__"
        
class WebsiteAdmin(admin.ModelAdmin):
    """
    Serializer for product view

    Args:
        ModelSerializer (Class): Basic serializer model
    """

    class Meta:
        """
        Meta for ProductSerializer class
        """

        model = Website
        fields = "__all__"

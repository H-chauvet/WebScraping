from django.contrib import admin
from .models import Product, Website, Category
from .serializers import ProductAdmin, WebsiteAdmin, CategoryAdmin


admin.site.register(Product, ProductAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(Category, CategoryAdmin)

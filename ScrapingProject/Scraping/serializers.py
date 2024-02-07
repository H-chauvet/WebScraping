from rest_framework import serializers
from .models import Article
from django.contrib import admin


class ArticleAdmin(admin.ModelAdmin):
    search_fields = ["Field1"]
    list_filter = ["Field1"]

    class Meta:
        model = Article
        fields = "__all__"

from django.contrib import admin
from .models import Article
from .serializers import ArticleAdmin


admin.site.register(Article, ArticleAdmin)

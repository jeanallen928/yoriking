from django.contrib import admin
from articles.models import Article, Category, Comment


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)

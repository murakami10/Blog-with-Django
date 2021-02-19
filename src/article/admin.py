from django.contrib import admin

from .models import Article
from .models import ArticleCategory
from .models import User

admin.site.register(Article)
admin.site.register(ArticleCategory)
admin.site.register(User)

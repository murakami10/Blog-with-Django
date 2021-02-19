from datetime import datetime

from django.db import models


class ArticleCategory(models.Model):
    class Meta:
        db_table = "article_category"

    category = models.CharField(verbose_name="カテゴリー", max_length=20)

    def __str__(self):
        return self.category


class User(models.Model):
    class Meta:
        db_table = "user"

    name = models.CharField(verbose_name="name", max_length=20)

    def __str__(self):
        return self.name


class Article(models.Model):
    class Meta:
        db_table = "article"

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="作者")
    title = models.CharField(verbose_name="タイトル", max_length=255)
    summary = models.CharField(verbose_name="記事の要約", max_length=255)
    content = models.TextField(verbose_name="内容")
    publish_date = models.DateTimeField(verbose_name="作成日")
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

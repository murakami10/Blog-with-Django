from django.contrib.auth import get_user_model
from django.db import transaction
from django.db import utils
from django.test import TestCase
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory


class ArticleCategoryTest(TestCase):
    def test_create_category(self):
        category = ArticleCategory.objects.create(category="python")
        self.assertEqual(category.category, "python")
        self.assertNotEqual(category.category, "Python")
        self.assertNotEqual(category.category, " python")
        with self.assertRaises(utils.IntegrityError):
            with transaction.atomic():
                ArticleCategory.objects.create(category="python")
            with transaction.atomic():
                ArticleCategory.objects.create(category="python")
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                ArticleCategory.objects.create(
                    category="aiueoaiueoaiueoaiueoa",
                )


class ArticleTest(TestCase):
    def test_create_article(self):
        c = ArticleCategory.objects.create(category="python")
        user = get_user_model()
        u = user.objects.create_user(email="test@test.com", password="test")
        article = Article.objects.create(
            author=u,
            title="python tour",
            summary="python is good",
            content="python is good lang",
            publish_date=timezone.now(),
            category=c,
        )
        self.assertEqual(article.author.email, u.email)
        self.assertEqual(article.title, "python tour")
        self.assertEqual(article.summary, "python is good")
        self.assertEqual(article.content, "python is good lang")
        self.assertEqual(article.category.category, c.category)
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                Article.objects.create(
                    author=u,
                    title="p" * 256,
                    summary="python is good",
                    content="python is good lang",
                    publish_date=timezone.now(),
                    category=c,
                )
        with self.assertRaises(utils.DataError):
            with transaction.atomic():
                Article.objects.create(
                    author=u,
                    title="p",
                    summary="p" * 256,
                    content="python is good lang",
                    publish_date=timezone.now(),
                    category=c,
                )

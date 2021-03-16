from django.contrib.auth import get_user_model
from django.db import utils
from django.test import TestCase
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory
from article.models import Tag


class ArticleCategoryTest(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(name="python")

    def test_make_same_category(self):
        with self.assertRaises(utils.IntegrityError):
            ArticleCategory.objects.create(name="python")

    def test_category_length_is_over(self):
        with self.assertRaises(utils.DataError):
            ArticleCategory.objects.create(
                name="aiueoaiueoaiueoaiueoa",
            )


class ArticleTest(TestCase):
    def setUp(self) -> None:
        self.c = ArticleCategory.objects.create(name="python")
        self.t = Tag.objects.create(name="php")
        user = get_user_model()
        self.u = user.objects.create_user(email="test@test.com", password="test")
        self.u2 = user.objects.create_user(email="test2@test2.com", password="test2")

        self.article = Article.objects.create(
            author=self.u,
            title="python tour",
            summary="python is good",
            content="python is good lang",
            publish_date=timezone.now() + timezone.timedelta(days=-1),
            public=True,
            category=self.c,
        )
        self.article.tag.add(self.t)

        self.article_future = Article.objects.create(
            author=self.u,
            title="python tour",
            summary="python is good",
            content="python is good lang",
            publish_date=timezone.now() + timezone.timedelta(days=1),
            public=True,
            category=self.c,
        )
        self.article_future.tag.add(self.t)

    def test_create_article(self):

        self.assertEqual(self.article.author.email, self.u.email)
        self.assertEqual(self.article.title, "python tour")
        self.assertEqual(self.article.summary, "python is good")
        self.assertEqual(self.article.content, "python is good lang")
        self.assertEqual(self.article.category.name, self.c.name)

    def test_title_length_is_over(self):

        with self.assertRaises(utils.DataError):
            Article.objects.create(
                author=self.u,
                title="p" * 256,
                summary="python is good",
                content="python is good lang",
                publish_date=timezone.now(),
                category=self.c,
            )

    def test_summary_length_is_over(self):

        with self.assertRaises(utils.DataError):
            Article.objects.create(
                author=self.u,
                title="p",
                summary="p" * 256,
                content="python is good lang",
                publish_date=timezone.now(),
                category=self.c,
            )

    def test_article_is_in_future(self):
        self.assertFalse(self.article.is_in_future())
        self.assertTrue(self.article_future.is_in_future())

    def test_set_author(self):
        self.assertEqual(self.article.author, self.u)
        self.article.set_author(self.u2)
        self.assertEqual(self.article.author, self.u2)

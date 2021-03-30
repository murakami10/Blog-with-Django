from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory
from article.models import Tag


class ArticleCategoryTests(TestCase):
    pass


class TagTests(TestCase):
    pass


class ArticleTests(TestCase):
    def setUp(self) -> None:
        user = get_user_model()
        self.u = user.objects.create_user(email="test@test.com", password="test")
        self.u2 = user.objects.create_user(email="test2@test.com", password="test2")

        self.c = ArticleCategory.objects.create(name="python")
        self.t = Tag.objects.create(name="php")

    def test_article_is_in_future(self):

        article = dict()
        keys = ["yesterday", "tomorrow", "ten_minutes"]

        for key, time in zip(keys, [{"days": -1}, {"days": 1}, {"minutes": 10}]):
            article[key] = Article.objects.create(
                author=self.u,
                title="python tour " + key,
                summary="python is good " + key,
                content="python is good lang " + key,
                publish_date=timezone.now() + timezone.timedelta(**time),
                public=True,
                category=self.c,
            )
            article[key].tag.add(self.t)

        keys = ["yesterday", "tomorrow", "ten_minutes"]
        self.assertFalse(article[keys[0]].is_in_future())
        self.assertTrue(article[keys[1]].is_in_future())
        self.assertTrue(article[keys[2]].is_in_future())

    def test_set_author(self):
        article = Article.objects.create(
            author=self.u,
            title="python tour ",
            summary="python is good ",
            content="python is good lang ",
            publish_date=timezone.now() + timezone.timedelta(days=1),
            public=True,
            category=self.c,
        )
        article.tag.add(self.t)

        self.assertEqual(article.author, self.u)
        article.set_author(self.u2)
        self.assertEqual(article.author, self.u2)

    def test_publish_article(self):
        article = Article.objects.create(
            author=self.u,
            title="python tour ",
            summary="python is good ",
            content="python is good lang ",
            publish_date=timezone.now() + timezone.timedelta(days=1),
            public=False,
            category=self.c,
        )
        article.tag.add(self.t)

        self.assertFalse(article.public)
        article.publish_article()
        self.assertTrue(article.public)

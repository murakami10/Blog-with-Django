from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory


class IndexViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(category="python")
        # 公開記事
        data = {
            "author": self.user,
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": True,
            "category": self.category,
        }
        self.article = Article.objects.create(**data)

        # 非公開記事
        data_not_public = {
            "author": self.user,
            "title": "second python",
            "summary": "python is bad",
            "content": "python is bad language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": False,
            "category": self.category,
        }
        self.article_not_public = Article.objects.create(**data_not_public)

        # 公開予定記事
        data_in_future = {
            "author": self.user,
            "title": "third python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category,
        }
        self.article_in_future = Article.objects.create(**data_in_future)

    def test_display_article(self):
        response = self.client.get(reverse("article:index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python")
        self.assertNotContains(response, "second python")
        self.assertNotContains(response, "third python")


class DetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(category="python")

        # 公開記事
        data = {
            "id": 1,
            "author": self.user,
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": True,
            "category": self.category,
        }
        self.article = Article.objects.create(**data)

        # 非公開記事
        data_not_public = {
            "id": 2,
            "author": self.user,
            "title": "second python",
            "summary": "python is bad",
            "content": "python is bad language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": False,
            "category": self.category,
        }
        self.article_not_public = Article.objects.create(**data_not_public)

        # 公開予定記事
        data_in_future = {
            "id": 3,
            "author": self.user,
            "title": "third python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category,
        }
        self.article_in_future = Article.objects.create(**data_in_future)

    def test_access_article_success(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python")

    def test_access_not_public_article_redirect(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 2}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:index"))

    def test_access_future_article_redirect(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 3}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:index"))


class CategoryViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category1 = ArticleCategory.objects.create(category="python")
        self.category2 = ArticleCategory.objects.create(category="ruby")

        self.article = {}
        self.article_not_public = {}
        self.article_in_future = {}

        for name, category in zip(["c1", "c2"], [self.category1, self.category2]):

            # 公開記事
            data = {
                "author": self.user,
                "title": "first python " + name,
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
                "category": category,
            }
            self.article[name] = Article.objects.create(**data)

            # 非公開記事
            data_not_public = {
                "author": self.user,
                "title": "second python " + name,
                "summary": "python is bad",
                "content": "python is bad language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": False,
                "category": category,
            }
            self.article_not_public[name] = Article.objects.create(**data_not_public)

            # 公開予定記事
            data_not_public = {
                "author": self.user,
                "title": "third python " + name,
                "summary": "python is soso",
                "content": "python is normal language",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
                "category": category,
            }

            self.article_in_future[name] = Article.objects.create(**data_not_public)

    def test_display_article(self):
        response = self.client.get(
            reverse("article:category", kwargs={"category": "python"})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python c1")
        self.assertNotContains(response, "second python c1")
        self.assertNotContains(response, "third python c1")

        self.assertNotContains(response, "first python c2")
        self.assertNotContains(response, "second python c2")
        self.assertNotContains(response, "third python c2")

        response = self.client.get(
            reverse("article:category", kwargs={"category": "ruby"})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "first python c1")
        self.assertNotContains(response, "second python c1")
        self.assertNotContains(response, "third python c1")

        self.assertContains(response, "first python c2")
        self.assertNotContains(response, "second python c2")
        self.assertNotContains(response, "third python c2")

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory
from article.models import Tag


class IndexViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")
        self.tag = Tag.objects.create(name="php")

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
        self.article.tag.add(self.tag)

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
        self.article_not_public.tag.add(self.tag)

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
        self.article_in_future.tag.add(self.tag)

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
        self.category = ArticleCategory.objects.create(name="python")
        self.tag = Tag.objects.create(name="php")

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
        self.article.tag.add(self.tag)

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
        self.article_not_public.tag.add(self.tag)

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
        self.article_in_future.tag.add(self.tag)

    def test_access_article_success(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python")

    # 次の記事と前の記事が表示される
    def test_display_next_pre_article(self):

        pre_data = {
            "id": 4,
            "author": self.user,
            "title": "pre title",
            "summary": "python is pre good",
            "content": "python is pre language",
            "publish_date": timezone.now() + timezone.timedelta(days=-2),
            "public": True,
            "category": self.category,
        }
        pre_article = Article.objects.create(**pre_data)
        pre_article.tag.add(self.tag)

        next_data = {
            "id": 5,
            "author": self.user,
            "title": "next title",
            "summary": "python is next good",
            "content": "python is next language",
            "publish_date": timezone.now() + timezone.timedelta(hours=-12),
            "public": True,
            "category": self.category,
        }
        next_article = Article.objects.create(**next_data)
        next_article.tag.add(self.tag)

        response = self.client.get(reverse("article:detail", kwargs={"article_id": 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "next title")
        self.assertContains(response, "pre title")

        response = self.client.get(
            reverse("article:detail", kwargs={"article_id": pre_data["id"]})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "pre title")
        self.assertContains(response, "first python")
        self.assertNotContains(response, "next title")

        response = self.client.get(
            reverse("article:detail", kwargs={"article_id": next_data["id"]})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "pre title")
        self.assertContains(response, "first python")
        self.assertContains(response, "next title")

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
        self.category1 = ArticleCategory.objects.create(name="python")
        self.category2 = ArticleCategory.objects.create(name="ruby")

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
            data_in_future = {
                "author": self.user,
                "title": "third python " + name,
                "summary": "python is soso",
                "content": "python is normal language",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
                "category": category,
            }

            self.article_in_future[name] = Article.objects.create(**data_in_future)

    def test_display_article(self):
        response = self.client.get(
            reverse("article:category", kwargs={"category": "python"})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "pythonカテゴリを選択")
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
        self.assertContains(response, "rubyカテゴリを選択")
        self.assertNotContains(response, "second python c2")
        self.assertNotContains(response, "third python c2")


class TagViewTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="program")

        self.tag1 = Tag.objects.create(name="python")
        self.tag2 = Tag.objects.create(name="ruby")

        self.article = {}
        self.article_not_public = {}
        self.article_in_future = {}

        for name, tag in zip(["t1", "t2"], [self.tag1, self.tag2]):

            # 公開記事
            data = {
                "author": self.user,
                "title": "first python " + name,
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
                "category": self.category,
            }
            self.article[name] = Article.objects.create(**data)
            self.article[name].tag.add(tag)

            # 非公開記事
            data_not_public = {
                "author": self.user,
                "title": "second python " + name,
                "summary": "python is bad",
                "content": "python is bad language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": False,
                "category": self.category,
            }
            self.article_not_public[name] = Article.objects.create(**data_not_public)
            self.article_not_public[name].tag.add(tag)

            # 公開予定記事
            data_in_future = {
                "author": self.user,
                "title": "third python " + name,
                "summary": "python is soso",
                "content": "python is normal language",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
                "category": self.category,
            }

            self.article_in_future[name] = Article.objects.create(**data_in_future)
            self.article_in_future[name].tag.add(tag)

    def test_display_article(self):
        response = self.client.get(reverse("article:tag", kwargs={"tag": "python"}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "pythonタグを選択")
        self.assertContains(response, "first python t1")
        self.assertNotContains(response, "second python t1")
        self.assertNotContains(response, "third python t1")

        self.assertNotContains(response, "first python t2")
        self.assertNotContains(response, "second python t2")
        self.assertNotContains(response, "third python t2")

        response = self.client.get(reverse("article:tag", kwargs={"tag": "ruby"}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "first python t1")
        self.assertNotContains(response, "second python t1")
        self.assertNotContains(response, "third python t1")

        self.assertContains(response, "first python t2")
        self.assertContains(response, "rubyタグを選択")
        self.assertNotContains(response, "second python t2")
        self.assertNotContains(response, "third python t2")

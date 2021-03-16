from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory


class LoginViewTests(TestCase):
    def setUp(self) -> None:
        get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )

    def test_login_sucsess(self):
        response = self.client.post(
            reverse("article:login"),
            data={"email": "test@test.com", "password": "aiueoaiueo"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))

    def test_login_error(self):
        response = self.client.post(
            reverse("article:login"),
            data={"email": "test@test.com", "password": "pythonpython"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Eメールアドレス または パスワードに誤りがあります.")

        response = self.client.post(
            reverse("article:login"),
            data={"email": "tete@tete.com", "password": "aiueoaiueo"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Eメールアドレス または パスワードに誤りがあります.")


class IndexViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")

    def test_display_public_article_success(self):
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

        # self.client.login(email="test@test.com", password="aiueoaiueo")
        self.client.force_login(self.user)
        response = self.client.get(reverse("article:login_index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python")
        self.assertContains(response, "edit")
        self.assertContains(response, "delete")
        self.assertNotContains(response, "非公開")
        self.assertNotContains(response, "公開予定")

    def test_display_not_public_article_success(self):

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

        self.client.force_login(self.user)
        response = self.client.get(reverse("article:login_index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "second python")
        self.assertContains(response, "edit")
        self.assertContains(response, "delete")
        self.assertContains(response, "非公開")
        self.assertNotContains(response, "公開予定")

    def test_display_article_in_future_success(self):

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

        self.client.force_login(self.user)
        response = self.client.get(reverse("article:login_index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "third python")
        self.assertContains(response, "edit")
        self.assertContains(response, "delete")
        self.assertNotContains(response, "非公開")
        self.assertContains(response, "公開予定")

    def test_login_index_error(self):
        response = self.client.get(reverse("article:login_index"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class AddArticleViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")
        self.client.force_login(self.user)

    def test_add_article_success(self):

        # 公開予定記事
        data = {
            "author": self.user,
            "title": "third python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category.pk,
        }

        response = self.client.post(
            reverse("article:post"),
            data=data,
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))

        response = self.client.get(reverse("article:login_index"))
        self.assertContains(response, "third python")
        self.assertContains(response, "公開予定")

    def test_add_past_article_error(self):

        # 過去の日付の記事
        data = {
            "author": self.user,
            "title": "third python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": True,
            "category": self.category.pk,
        }

        response = self.client.post(
            reverse("article:post"),
            data=data,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "過去の日付になっています.")

        response = self.client.get(reverse("article:login_index"))
        self.assertNotContains(response, "third python")


class AddCategoryViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")

    def test_login_add_category_success(self):

        self.client.force_login(self.user)
        self.assertEqual(ArticleCategory.objects.count(), 1)
        response = self.client.post(
            reverse("article:add_category"),
            data={"name": "django"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertTrue(ArticleCategory.objects.filter(name="django").exists())
        self.assertEqual(ArticleCategory.objects.count(), 2)

    def test_login_add_category_error(self):

        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article:add_category"),
            data={"name": "python"},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "すでにそのカテゴリは存在してます.")

        response = self.client.post(
            reverse("article:add_category"),
            data={"name": ""},
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "このフィールドは必須です")

    def test_add_category_without_login(self):
        response = self.client.post(
            reverse("article:add_category"),
            data={"name": "django"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.assertFalse(ArticleCategory.objects.filter(name="django").exists())


class DeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")
        data = {
            "author": self.user,
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category,
        }
        self.article = Article.objects.create(**data)
        self.client.force_login(self.user)

    def test_delete_article_sucess(self):

        response = self.client.get(reverse("article:login_index"))
        self.assertContains(response, "first python")

        response = self.client.post(
            reverse("article:login_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get(reverse("article:login_index"))
        self.assertNotContains(response, "first python")


class EditViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        self.category = ArticleCategory.objects.create(name="python")
        data = {
            "author": self.user,
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category,
        }
        self.article = Article.objects.create(**data)

    def test_edit_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article:login_edit", kwargs={"article_id": self.article.pk}),
            data={
                "title": "second python",
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
                "category": self.category.id,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))

    def test_edit_article_past_day_success(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article:login_edit", kwargs={"article_id": self.article.pk}),
            data={
                "title": "second python",
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
                "category": self.category.id,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))

        response = self.client.get(reverse("article:login_index"))

        self.assertContains(response, "second python")
        self.assertNotContains(response, "非公開")
        self.assertNotContains(response, "公開予定")

    def test_edit_error(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("article:login_edit", kwargs={"article_id": self.article.pk}),
            data={
                "title": "second python",
                "summary": "python is good",
                "content": "python is good language",
                "public": True,
                "publish_date": timezone.now() + timezone.timedelta(days=1),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "このフィールドは必須です")

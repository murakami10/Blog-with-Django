from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory
from article.models import Tag
from article.models import User
from article.views.views_login import CategoryView
from article.views.views_login import IndexView
from article.views.views_login import TagView


class LoginViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")

    def test_access_index_without_login_no(self):
        response = self.client.get(reverse("article:login_index"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_display_public_article_ok(self):
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
        for content in ["first python", "edit", "delete"]:
            with self.subTest(msg="response doesn't contain " + content):
                self.assertContains(response, content)

        for content in ["非公開", "公開予定"]:
            with self.subTest(msg="response contain " + content):
                self.assertNotContains(response, content)

    def test_display_not_public_article_ok(self):

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
        for content in ["second python", "edit", "delete", "非公開"]:
            with self.subTest(msg="response doesn't contain " + content):
                self.assertContains(response, content)

        self.assertNotContains(response, "公開予定")

    def test_display_article_in_future_ok(self):

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
        for content in ["third python", "edit", "delete", "公開予定"]:
            with self.subTest(msg="response doesn't contain " + content):
                self.assertContains(response, content)

        self.assertNotContains(response, "非公開")

    def test_pagination_of_latest_article_ok(self):

        # 新しい記事をIndexView.article_per_page + 2作成
        num_of_article = IndexView.article_per_page + 2
        for index in range(num_of_article):
            data = {
                "author": self.user,
                "title": "python " + str(index),
                "summary": "python is good " + str(index),
                "content": "python is good language " + str(index),
                "publish_date": timezone.now() - timezone.timedelta(minutes=index),
                "public": True,
                "category": self.category,
            }
            Article.objects.create(**data)

        response = self.client.get(reverse("article:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        for index in range(IndexView.article_per_page):
            with self.subTest(msg="response not contain " + str(index) + " article"):
                self.assertContains(response, "python " + str(index))

        for index in range(IndexView.article_per_page + 1, num_of_article):
            with self.subTest(msg="response contain " + str(index) + " article"):
                self.assertNotContains(response, "python " + str(index))


class PostArticleViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")
        cls.tag1 = Tag.objects.create(name="tag1")
        cls.tag2 = Tag.objects.create(name="tag2")

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_post_article_ok(self):

        # 公開予定記事
        data = {
            "author": self.user,
            "title": "first python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": self.category.pk,
            "tag": (self.tag1.id,),
        }

        num_of_article = Article.objects.count()

        response = self.client.post(reverse("article:post"), data=data,)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertEqual(Article.objects.count(), num_of_article + 1)

        response = self.client.get(reverse("article:login_index"))
        self.assertContains(response, "first python")
        self.assertContains(response, "公開予定")

    def test_post_past_article_no(self):

        # 過去の日付の記事
        data = {
            "author": self.user,
            "title": "second python",
            "summary": "python is soso",
            "content": "python is normal language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": True,
            "category": self.category.pk,
        }

        num_of_article = Article.objects.count()

        response = self.client.post(reverse("article:post"), data=data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Article.objects.count(), num_of_article)
        self.assertContains(response, "過去の日付になっています.")

        response = self.client.get(reverse("article:login_index"))
        self.assertNotContains(response, "second python")


class AddCategoryViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_add_category_ok(self):

        num_of_category = ArticleCategory.objects.count()

        response = self.client.post(
            reverse("article:add_category"), data={"name": "django"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertTrue(ArticleCategory.objects.filter(name="django").exists())
        self.assertEqual(ArticleCategory.objects.count(), num_of_category + 1)

    def test_add_same_name_category_no(self):

        num_of_category = ArticleCategory.objects.count()

        response = self.client.post(
            reverse("article:add_category"), data={"name": "python"}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "すでにそのカテゴリは存在してます.")
        self.assertEqual(ArticleCategory.objects.count(), num_of_category)

    def test_add_empty_name_category_no(self):

        num_of_category = ArticleCategory.objects.count()

        response = self.client.post(reverse("article:add_category"), data={"name": ""})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "このフィールドは必須です")
        self.assertEqual(ArticleCategory.objects.count(), num_of_category)


class AddTagViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="program")
        cls.tag1 = Tag.objects.create(name="python")
        cls.tag2 = Tag.objects.create(name="php")

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_add_tag_ok(self):

        num_of_tag = Tag.objects.count()

        response = self.client.post(
            reverse("article:add_tag"), data={"name": "django"},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertTrue(Tag.objects.filter(name="django").exists())
        self.assertEqual(Tag.objects.count(), num_of_tag + 1)

    def test_add_same_name_tag_no(self):

        num_of_tag = Tag.objects.count()
        response = self.client.post(reverse("article:add_tag"), data={"name": "python"})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "すでにそのタグは存在してます.")
        self.assertEqual(Tag.objects.count(), num_of_tag)

    def test_add_empty_name_category_no(self):
        num_of_tag = Tag.objects.count()

        response = self.client.post(reverse("article:add_tag"), data={"name": ""})

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "このフィールドは必須です")
        self.assertEqual(Tag.objects.count(), num_of_tag)


class DeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")
        data = {
            "author": cls.user,
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "public": True,
            "category": cls.category,
        }
        cls.article = Article.objects.create(**data)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_article_ok(self):

        response = self.client.get(reverse("article:login_index"))
        self.assertContains(response, "first python")

        num_of_article = Article.objects.count()

        response = self.client.post(
            reverse("article:login_delete", kwargs={"pk": self.article.pk})
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get(reverse("article:login_index"))
        self.assertNotContains(response, "first python")
        self.assertEqual(Article.objects.count(), num_of_article - 1)


class EditViewTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")
        cls.tag = Tag.objects.create(name="tag")

    def setUp(self) -> None:
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
        self.article.tag.add(self.tag)
        self.client.force_login(self.user)

    def test_edit_article_ok(self):

        num_of_article = Article.objects.count()
        self.assertFalse(Article.objects.filter(title="second python").exists())

        response = self.client.post(
            reverse("article:login_edit", kwargs={"article_id": self.article.pk}),
            data={
                "title": "second python",
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
                "category": self.category.id,
                "tag": (),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertEqual(Article.objects.count(), num_of_article)
        self.assertTrue(Article.objects.filter(title="second python").exists())

    def test_edit_article_past_day_ok(self):

        num_of_article = Article.objects.count()
        self.assertFalse(Article.objects.filter(title="past python").exists())

        response = self.client.post(
            reverse("article:login_edit", kwargs={"article_id": self.article.pk}),
            data={
                "title": "past python",
                "summary": "python is good",
                "content": "python is good language",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
                "category": self.category.id,
                "tag": (),
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:login_index"))
        self.assertEqual(Article.objects.count(), num_of_article)
        self.assertTrue(Article.objects.filter(title="past python").exists())


class CategoryViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category1 = ArticleCategory.objects.create(name="python")
        cls.category2 = ArticleCategory.objects.create(name="ruby")

        cls.tag = Tag.objects.create(name="php")

        cls.data_diff = {
            # 公開記事
            "public": {
                "title": "public article",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
            },
            # 未公開記事
            "not_public": {
                "title": "not public article",
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": False,
            },
            # 公開予定の記事
            "future": {
                "title": "future article",
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
            },
        }

        cls.articles = {}
        for category in [cls.category1, cls.category2]:
            for key, value in cls.data_diff.items():
                data = {
                    "author": cls.user,
                    "title": value["title"] + category.name,
                    "summary": "python is good t1 " + category.name,
                    "content": "python is good language t1 " + category.name,
                    "publish_date": value["publish_date"],
                    "public": value["public"],
                    "category": category,
                }
                cls.articles[category.name + key] = Article.objects.create(**data)
                cls.articles[category.name + key].tag.add(cls.tag)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_display_article_filtered_with_category_ok(self):
        response = self.client.get(
            reverse("article:login_category", kwargs={"category": self.category1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        content_contain = [
            "pythonカテゴリを選択",
            self.data_diff["public"]["title"] + self.category1.name,
            self.data_diff["not_public"]["title"] + self.category1.name,
            self.data_diff["future"]["title"] + self.category1.name,
        ]
        content_not_contain = [
            self.data_diff["public"]["title"] + self.category2.name,
            self.data_diff["not_public"]["title"] + self.category2.name,
            self.data_diff["future"]["title"] + self.category2.name,
        ]

        for value in content_contain:
            with self.subTest(msg="response doesn't contain ", value=value):
                self.assertContains(response, value)

        for value in content_not_contain:
            with self.subTest(msg="response contain", value=value):
                self.assertNotContains(response, value)

    def test_pagination_of_latest_article_filtered_with_category_ok(self):

        # カテゴリが違う記事をぞれぞれCategoryView.article_per_page Article.objects.filter(category=self.category1).count() + 2作成
        num_of_article = CategoryView.article_per_page + 2
        day_after_tommorrow = timezone.now() + timezone.timedelta(days=2)
        for index in range(num_of_article):
            for category in [self.category1, self.category2]:
                data = {
                    "author": self.user,
                    "title": category.name + "python" + str(index),
                    "summary": "python is good " + str(index),
                    "content": "python is good language " + str(index),
                    "publish_date": day_after_tommorrow
                    - timezone.timedelta(minutes=index),
                    "public": True,
                    "category": category,
                }
                article = Article.objects.create(**data)
                article.tag.add(self.tag)

        response = self.client.get(
            reverse("article:login_category", kwargs={"category": self.category1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        # 表示件数がCategoryView.article_per_pageで有ることを確認
        for index in range(CategoryView.article_per_page):
            with self.subTest(
                msg="response not contain " + str(index) + " article", category="c1"
            ):
                self.assertContains(
                    response, self.category1.name + "python" + str(index)
                )

        for index in range(CategoryView.article_per_page + 1, num_of_article):
            with self.subTest(
                msg="response contain " + str(index) + " article", category="c1"
            ):
                self.assertNotContains(
                    response, self.category1.name + "python" + str(index)
                )


class TagViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="program")

        cls.tag1 = Tag.objects.create(name="python")
        cls.tag2 = Tag.objects.create(name="ruby")

        cls.articles_c1 = {}

        now = timezone.now()
        cls.data_diff = {
            # 公開記事
            "public": {
                "title": "public article",
                "publish_date": now + timezone.timedelta(days=-1),
                "public": True,
            },
            # 未公開記事
            "not_public": {
                "title": "not public article",
                "publish_date": now + timezone.timedelta(days=-1),
                "public": False,
            },
            # 公開予定の記事
            "future": {
                "title": "future article",
                "publish_date": now + timezone.timedelta(days=1),
                "public": True,
            },
        }

        cls.articles = {}
        for tag in [cls.tag1, cls.tag2]:
            for key, value in cls.data_diff.items():
                data = {
                    "author": cls.user,
                    "title": value["title"] + tag.name,
                    "summary": "python is good t1 " + tag.name,
                    "content": "python is good language t1 " + tag.name,
                    "publish_date": value["publish_date"],
                    "public": value["public"],
                    "category": cls.category,
                }
                cls.articles[tag.name + key] = Article.objects.create(**data)
                cls.articles[tag.name + key].tag.add(tag)

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_display_article_filtered_with_tag_ok(self):
        response = self.client.get(
            reverse("article:login_tag", kwargs={"tag": self.tag1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_contain = [
            self.tag1.name + "タグを選択",
            self.data_diff["public"]["title"] + self.tag1.name,
            self.data_diff["not_public"]["title"] + self.tag1.name,
            self.data_diff["future"]["title"] + self.tag1.name,
        ]
        response_not_contain = [
            self.data_diff["public"]["title"] + self.tag2.name,
            self.data_diff["not_public"]["title"] + self.tag2.name,
            self.data_diff["future"]["title"] + self.tag2.name,
        ]

        for value in response_contain:
            with self.subTest(msg="response doesn't contain ", value=value):
                self.assertContains(response, value)

        for value in response_not_contain:
            with self.subTest(msg="response contain", value=value):
                self.assertNotContains(response, value)

    # 複数のタグを持った記事も表示
    def test_display_article_filtered_with_multitag_ok(self):

        title = "t1 and t2"

        data = {
            "author": self.user,
            "title": title,
            "summary": "python is good t1 ",
            "content": "python is good language t1 ",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "public": True,
            "category": self.category,
        }
        articles = Article.objects.create(**data)
        articles.tag.add(self.tag1)
        articles.tag.add(self.tag2)

        for tag in [self.tag1, self.tag2]:
            response = self.client.get(
                reverse("article:login_tag", kwargs={"tag": tag.name})
            )
            with self.subTest(tag=tag.name):
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, title)

    def test_pagination_of_latest_article_filtered_with_tag_ok(self):

        # タグが違う記事をぞれぞれTagView.article_per_page + 2作成
        num_of_article = TagView.article_per_page + 2
        day_after_tommorrow = timezone.now() + timezone.timedelta(days=2)
        for tag in [self.tag1, self.tag2]:
            for index in range(num_of_article):
                data = {
                    "author": self.user,
                    "title": tag.name + "python" + str(index),
                    "summary": "python is good " + str(index),
                    "content": "python is good language " + str(index),
                    "publish_date": day_after_tommorrow
                    - timezone.timedelta(minutes=index),
                    "public": True,
                    "category": self.category,
                }
                article = Article.objects.create(**data)
                article.tag.add(tag)

        response = self.client.get(
            reverse("article:login_tag", kwargs={"tag": self.tag1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        # 表示件数がTagView.article_per_pageで有ることを確認
        for index in range(TagView.article_per_page):
            with self.subTest(
                msg="response not contain " + str(index) + " article", tag="t1"
            ):
                self.assertContains(response, self.tag1.name + "python" + str(index))

        for index in range(TagView.article_per_page + 1, num_of_article):
            with self.subTest(
                msg="response contain " + str(index) + " article", tag="t1"
            ):
                self.assertNotContains(response, self.tag1.name + "python" + str(index))


class SettingViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo", username="tomtom"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_display_setting_page_ok(self):

        response = self.client.get(reverse("article:setting"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        content_included = [
            "ユーザ名を変更する",
            "メールアドレスを変更する",
            "パスワードを変更する",
            "新しくユーザを作成する",
        ]
        for content in content_included:
            with self.subTest(msg="response doesn't contain " + content):
                self.assertContains(response, content)


class ChangeUsernameViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo", username="tomtom"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_change_username_ok(self):

        change_name = "john"
        response = self.client.post(
            reverse("article:change_username"), data={"username": change_name},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(change_name, user.username)


class ChangeEmailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo", username="tomtom"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_change_email_ok(self):

        change_email = "aiueo@aiueo.com"
        response = self.client.post(
            reverse("article:change_email"), data={"email": change_email},
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        user = User.objects.get(id=self.user.id)
        self.assertEqual(change_email, user.email)


class ChangePasswordViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "aiueoaiueo"
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password=cls.password, username="tomtom"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_change_password_ok(self):
        new_password = "aiuo1347"
        response = self.client.post(
            reverse("article:change_password"),
            data={
                "old_password": self.password,
                "new_password1": new_password,
                "new_password2": new_password,
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.check_password(new_password))


class SignUpViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "aiueoaiueo"
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password=cls.password, username="tomtom"
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_sigh_up_user_ok(self):

        pre_count_user = User.objects.count()

        new_user = {
            "email": "test2@test.com",
            "password1": "uaar28ass",
            "password2": "uaar28ass",
            "username": "user2",
        }

        response = self.client.post(reverse("article:sign_up"), data=new_user)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(User.objects.count(), pre_count_user + 1)

        user = User.objects.get(username=new_user["username"])
        self.assertEqual(user.email, new_user["email"])
        self.assertTrue(user.check_password(new_user["password1"]))

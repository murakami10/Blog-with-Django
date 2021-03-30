from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from article.models import Article
from article.models import ArticleCategory
from article.models import Tag
from article.views.views_user import CategoryView
from article.views.views_user import IndexView
from article.views.views_user import TagView


class IndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")
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
        for key, value in cls.data_diff.items():
            # 公開記事
            data = {
                "author": cls.user,
                "title": value["title"],
                "summary": "python is good " + key,
                "content": "python is good language " + key,
                "publish_date": value["publish_date"],
                "public": value["public"],
                "category": cls.category,
            }
            cls.articles[key] = Article.objects.create(**data)
            cls.articles[key].tag.add(cls.tag)

    def test_display_public_article_ok(self):
        response = self.client.get(reverse("article:index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, self.data_diff["public"]["title"])

    def test_display_not_public_article_no(self):
        response = self.client.get(reverse("article:index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, self.data_diff["not_public"]["title"])

    def test_display_future_article_no(self):
        response = self.client.get(reverse("article:index"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, self.data_diff["future"]["title"])

    def test_pagination_of_latest_article_ok(self):

        # 新しい記事をIndex.article_per_page + 2作成
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
            article = Article.objects.create(**data)
            article.tag.add(self.tag)

        response = self.client.get(reverse("article:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        for index in range(IndexView.article_per_page):
            with self.subTest(msg="response not contain " + str(index) + " article"):
                self.assertContains(response, "python " + str(index))

        for index in range(IndexView.article_per_page + 1, num_of_article):
            with self.subTest(msg="response contain " + str(index) + " article"):
                self.assertNotContains(response, "python " + str(index))


class DetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_superuser(
            email="test@test.com", password="aiueoaiueo"
        )
        cls.category = ArticleCategory.objects.create(name="python")
        cls.tag = Tag.objects.create(name="php")

        cls.articles = {}
        data_diff = {
            # 公開記事
            "public": {
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": True,
            },
            # 未公開記事
            "not_public": {
                "publish_date": timezone.now() + timezone.timedelta(days=-1),
                "public": False,
            },
            # 公開予定の記事
            "future": {
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "public": True,
            },
        }
        for index, (key, value) in enumerate(data_diff.items(), 1):
            data = {
                "id": index,
                "author": cls.user,
                "title": "first python " + key,
                "summary": "python is good " + key,
                "content": "python is good language " + key,
                "publish_date": value["publish_date"],
                "public": value["public"],
                "category": cls.category,
            }
            cls.articles[key] = Article.objects.create(**data)
            cls.articles[key].tag.add(cls.tag)

    def test_access_public_article_ok(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 1}))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "first python")

    # 次の記事と前の記事が表示される
    def test_display_next_pre_article(self):

        # 現在公開されている記事より前の時間の記事を作成
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

        # 最新の記事を投稿
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

        # 次の記事と前の記事のタイトルが表示される
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 1}))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "next title")
        self.assertContains(response, "pre title")

        # 一番最初の記事のため次の記事のみ表示される
        response = self.client.get(
            reverse("article:detail", kwargs={"article_id": pre_data["id"]})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "pre title")
        self.assertContains(response, "first python")
        self.assertNotContains(response, "next title")

        # 一番最新の記事のため前の記事のみ表示される
        response = self.client.get(
            reverse("article:detail", kwargs={"article_id": next_data["id"]})
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotContains(response, "pre title")
        self.assertContains(response, "first python")
        self.assertContains(response, "next title")

    def test_access_not_public_article_no(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 2}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:index"))

    def test_access_future_article_no(self):
        response = self.client.get(reverse("article:detail", kwargs={"article_id": 3}))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], reverse("article:index"))


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

    def test_display_article_filtered_with_category_ok(self):
        response = self.client.get(
            reverse("article:category", kwargs={"category": self.category1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        content_contain = [
            self.category1.name + "カテゴリを選択",
            self.data_diff["public"]["title"] + self.category1.name,
        ]
        content_not_contain = [
            self.data_diff["not_public"]["title"] + self.category1.name,
            self.data_diff["future"]["title"] + self.category1.name,
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

        # カテゴリが違う記事をぞれぞれCategoryView.article_per_page + 2作成
        num_of_article = CategoryView.article_per_page + 2
        for category in [self.category1, self.category2]:
            for index in range(num_of_article):
                data = {
                    "author": self.user,
                    "title": category.name + "python" + str(index),
                    "summary": "python is good " + str(index),
                    "content": "python is good language " + str(index),
                    "publish_date": timezone.now() - timezone.timedelta(minutes=index),
                    "public": True,
                    "category": category,
                }
                article = Article.objects.create(**data)
                article.tag.add(self.tag)

        response = self.client.get(
            reverse("article:category", kwargs={"category": self.category1.name})
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
                    response, self.category1.name + "python c1 " + str(index)
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

    def test_display_article_filtered_with_tag_ok(self):
        response = self.client.get(
            reverse("article:tag", kwargs={"tag": self.tag1.name})
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        response_contain = [
            self.tag1.name + "タグを選択",
            self.data_diff["public"]["title"] + self.tag1.name,
        ]
        response_not_contain = [
            self.data_diff["not_public"]["title"] + self.tag1.name,
            self.data_diff["future"]["title"] + self.tag1.name,
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
            response = self.client.get(reverse("article:tag", kwargs={"tag": tag.name}))
            with self.subTest(tag=tag.name):
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertContains(response, title)

    def test_pagination_of_latest_article_filtered_with_tag_ok(self):

        # タグが違う記事をぞれぞれTagView.article_per_page + 2作成
        num_of_article = TagView.article_per_page + 2
        for tag in [self.tag1, self.tag2]:
            for index in range(num_of_article):
                data = {
                    "author": self.user,
                    "title": tag.name + "python" + str(index),
                    "summary": "python is good " + str(index),
                    "content": "python is good language " + str(index),
                    "publish_date": timezone.now() - timezone.timedelta(minutes=index),
                    "public": True,
                    "category": self.category,
                }
                article = Article.objects.create(**data)
                article.tag.add(tag)

        response = self.client.get(
            reverse("article:tag", kwargs={"tag": self.tag1.name})
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

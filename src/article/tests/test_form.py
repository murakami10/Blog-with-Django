from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from article.forms import AddCategoryForm
from article.forms import AddTagForm
from article.forms import EmailAuthenticationForm
from article.forms import PostArticleForm
from article.forms import PrepareArticleForm
from article.models import ArticleCategory
from article.models import Tag


class EmailAuthenticationFormTests(TestCase):
    def setUp(self) -> None:
        user = get_user_model()
        self.password = "aiueoaiueo"
        self.u = user.objects.create_user(
            email="test@test.com", password=self.password, username="phpperson"
        )

    def test_valid_form(self):
        data = {
            "email": self.u.email,
            "password": self.password,
        }
        form = EmailAuthenticationForm(data=data)

        self.assertTrue(form.is_valid())

    def test_username_instead_of_email(self):
        data = {
            "username": self.u.username,
            "password": self.password,
        }
        form = EmailAuthenticationForm(data=data)

        self.assertFalse(form.is_valid())


class PrepareArticleFormTests(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(name="python")
        self.tag = Tag.objects.create(name="tag")
        self.tag2 = Tag.objects.create(name="tag2")

    def test_valid_form(self):

        keys = ["no_tag", "one_tag", "two_tag"]
        data = dict()
        tags = ([], [self.tag], [self.tag, self.tag2])
        for key, tag in zip(keys, tags):
            data[key] = {
                "title": "first python " + key,
                "summary": "python is good " + key,
                "publish_date": timezone.now() + timezone.timedelta(days=1),
                "category": self.category,
                "tag": tag,
            }

        for key in keys:
            with self.subTest(msg="タグの数が変化", key=key):
                form = PrepareArticleForm(data[key])
                self.assertTrue(form.is_valid())

    def test_not_valid_data_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
            "tag": self.tag,
        }

        error_datas = {
            "title": "",
            "summary": "",
            "publish_date": "1999/09/09",
            "category": "python",
            "tag": "php",
        }

        for key, value in error_datas.items():
            with self.subTest(key=key, value=value):
                error_data = data.copy()
                error_data[key] = value
                form = PrepareArticleForm(error_data)
                self.assertFalse(form.is_valid())

    def test_not_valid_past_pubish_data(self):
        past_published_data = {
            "title": "first python",
            "summary": "python is good",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "category": self.category,
        }

        form = PrepareArticleForm(past_published_data)
        self.assertFalse(form.is_valid())


class AddCategoryFormTest(TestCase):
    def setUp(self) -> None:
        data = {"name": "python"}
        ArticleCategory.objects.create(**data)

    def test_valid_form(self):
        data = {"name": "django"}
        form = AddCategoryForm(data)
        self.assertTrue(form.is_valid())

    def test_is_not_valid_with_same_category_name(self):
        data = {"name": "python"}
        form = AddCategoryForm(data)
        self.assertFalse(form.is_valid())

    def test_is_not_valid_with_no_name(self):
        data = {"name": ""}
        form = AddCategoryForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"][0], "このフィールドは必須です。")


class AddTagFormTest(TestCase):
    def setUp(self) -> None:
        data = {"name": "python"}
        self.tag = Tag.objects.create(**data)

    def test_valid_form(self):
        data = {"name": "php"}
        form = AddTagForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_with_same_tag_name(self):
        data = {"name": "python"}
        form = AddTagForm(data)
        self.assertFalse(form.is_valid())

    def test_is_not_valid_with_no_name(self):
        data = {"name": ""}
        form = AddTagForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["name"][0], "このフィールドは必須です。")


class PostArticleFormTests(TestCase):
    def setUp(self) -> None:
        self.category = ArticleCategory.objects.create(name="python")
        self.tag = Tag.objects.create(name="php")

    def test_valid_form(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
            "tag": [self.tag.id],
        }

        form = PostArticleForm(data)
        self.assertTrue(form.is_valid())

    def test_valid_past_article_error(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=-1),
            "category": self.category,
            "tag": self.tag,
        }

        form = PostArticleForm(data)
        self.assertFalse(form.is_valid())

    def test_not_valid_form_with_various_data(self):
        data = {
            "title": "first python",
            "summary": "python is good",
            "content": "python is good language",
            "publish_date": timezone.now() + timezone.timedelta(days=1),
            "category": self.category,
        }

        error_datas = {
            "title": "",
            "summary": "",
            "content": "",
            "publish_date": "1999/09/09",
            "category": "python",
            "tag": "php",
        }
        for key, value in error_datas.items():
            with self.subTest(key=key, value=value):
                error_data = data.copy()
                error_data[key] = value
                form = PostArticleForm(error_data)
                self.assertFalse(form.is_valid())

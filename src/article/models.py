from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class ArticleCategory(models.Model):
    class Meta:
        db_table = "articles_categories"

    category = models.CharField(verbose_name="カテゴリー", max_length=20, unique=True)

    def __str__(self):
        return self.category


class User(AbstractUser):
    name_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _("name"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        default="no name",
        validators=[name_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Article(models.Model):
    class Meta:
        db_table = "articles"

    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="作者")
    title = models.CharField(verbose_name="タイトル", max_length=255)
    summary = models.CharField(verbose_name="記事の要約", max_length=255)
    content = models.TextField(verbose_name="内容")
    publish_date = models.DateTimeField(verbose_name="作成日")
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT)

    def __str__(self):
        return self.title

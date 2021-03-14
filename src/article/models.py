from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from mdeditor.fields import MDTextField

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
        default="no_name",
        validators=[name_validator],
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
    content = MDTextField()
    publish_date = models.DateTimeField(verbose_name="投稿日")
    public = models.BooleanField(verbose_name="公開状態", default=0)
    category = models.ForeignKey(ArticleCategory, on_delete=models.PROTECT)

    def set_author(self, user: User):
        self.author_id = user.id

    def publish_article(self):
        self.public = True

    def is_in_future(self):
        return self.publish_date >= timezone.now()

    def __str__(self):
        return self.title

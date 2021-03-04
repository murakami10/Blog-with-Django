from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.urls import path

from . import views

app_name = "article"
urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("<int:article_id>/detail/", views.DetailView.as_view(), name="detail"),
    path("prepare/", views.PrepareArticle.as_view(), name="prepare_post"),
    path("post/", views.PostArticle.as_view(), name="post"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("login/index/", views.LoginIndex.as_view(), name="login_index"),
    path(
        "login/<int:article_id>/detail/",
        views.LoginDetail.as_view(),
        name="login_detail",
    ),
    path(
        "login/<int:article_id>/edit/",
        views.LoginEdit.as_view(),
        name="login_edit",
    ),
    path(
        "login/<int:pk>/delete/",
        views.LoginDelete.as_view(),
        name="login_delete",
    ),
    url(r"mdeditor/", include("mdeditor.urls")),
]

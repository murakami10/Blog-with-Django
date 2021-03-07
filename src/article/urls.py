from django.conf.urls import include
from django.conf.urls import url
from django.urls import path

from .views import views_login
from .views import views_user

app_name = "article"
urlpatterns = [
    path("index/", views_user.IndexView.as_view(), name="index"),
    path(
        "<int:article_id>/detail/",
        views_user.DetailView.as_view(),
        name="detail",
    ),
    path(
        "prepare/",
        views_login.PrepareArticle.as_view(),
        name="prepare_post",
    ),
    path("post/", views_login.PostArticle.as_view(), name="post"),
    path("login/", views_login.Login.as_view(), name="login"),
    path("logout/", views_login.Logout.as_view(), name="logout"),
    path(
        "login/index/",
        views_login.LoginIndex.as_view(),
        name="login_index",
    ),
    path(
        "login/<int:article_id>/detail/",
        views_login.LoginDetail.as_view(),
        name="login_detail",
    ),
    path(
        "login/<int:article_id>/edit/",
        views_login.LoginEdit.as_view(),
        name="login_edit",
    ),
    path(
        "login/<int:pk>/delete/",
        views_login.LoginDeleteArticle.as_view(),
        name="login_delete",
    ),
    path(
        "login/add-article/",
        views_login.AddCategory.as_view(),
        name="add_category",
    ),
    url(r"mdeditor/", include("mdeditor.urls")),
]

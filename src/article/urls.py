from django.conf.urls import include
from django.conf.urls import url
from django.urls import path

from .views import views_login
from .views import views_user

app_name = "article"
urlpatterns = [
    path("index/", views_user.IndexView.as_view(), name="index"),
    path("<int:article_id>/detail/", views_user.DetailView.as_view(), name="detail"),
    path(
        "index/categories/<str:category>/",
        views_user.CategoryView.as_view(),
        name="category",
    ),
    path("prepare/", views_login.PrepareArticle.as_view(), name="prepare_post"),
    path("post/", views_login.PostArticle.as_view(), name="post"),
    path("login/", views_login.Login.as_view(), name="login"),
    path("logout/", views_login.Logout.as_view(), name="logout"),
    path("login/index/", views_login.Index.as_view(), name="login_index"),
    path(
        "login/<int:article_id>/detail/",
        views_login.Detail.as_view(),
        name="login_detail",
    ),
    path(
        "login/<int:article_id>/edit/",
        views_login.Edit.as_view(),
        name="login_edit",
    ),
    path(
        "login/<int:pk>/delete/",
        views_login.Delete.as_view(),
        name="login_delete",
    ),
    path(
        "login/add-category/",
        views_login.AddCategoryView.as_view(),
        name="add_category",
    ),
    path("login/add-tag/", views_login.AddTagView.as_view(), name="add_tag"),
    path(
        "login/index/categories/<str:category>/",
        views_login.CategoryView.as_view(),
        name="login_category",
    ),
    url(r"mdeditor/", include("mdeditor.urls")),
]

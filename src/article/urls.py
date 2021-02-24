from django.urls import path

from . import views

app_name = "article"
urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("detail/<int:article_id>/", views.DetailView.as_view(), name="detail"),
    path("post/", views.PostArticle.as_view(), name="post"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
]

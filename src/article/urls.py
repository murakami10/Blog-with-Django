from django.conf import settings
from django.conf.urls import include
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "article"
urlpatterns = [
    path("index/", views.IndexView.as_view(), name="index"),
    path("detail/<int:article_id>/", views.DetailView.as_view(), name="detail"),
    path("post/", views.PostArticle.as_view(), name="post"),
    path("login/", views.Login.as_view(), name="login"),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("login/index/", views.LoginIndex.as_view(), name="login_index"),
    path(
        "login/detail/<int:article_id>/",
        views.LoginDetail.as_view(),
        name="login_detail",
    ),
    url(r"mdeditor/", include("mdeditor.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path

from .views import DetailView
from .views import IndexView

app_name = "article"
urlpatterns = [
    path("index/", IndexView.as_view(), name="index"),
    path("detail/<int:article_id>/", DetailView.as_view(), name="detail"),
]

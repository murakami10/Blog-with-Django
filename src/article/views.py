from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View

from .models import Article


class IndexView(View):
    def get(self, request):
        latest_article_list = Article.objects.order_by("-publish_date")[:5]
        context = {"latest_article_list": latest_article_list}
        return render(request, "article/index.html", context)


class DetailView(View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        return render(request, "article/detail.html", {"article": article})

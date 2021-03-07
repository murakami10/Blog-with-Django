from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from article.models import Article
from article.models import ArticleCategory


class IndexView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect("article:login_index")

        latest_article_list = (
            Article.objects.order_by("-publish_date")[:5]
            .select_related()
            .values(
                "id",
                "title",
                "author__username",
                "summary",
                "publish_date",
                "category__category",
            )
        )
        context = {
            "latest_article_list": latest_article_list,
            "category": ArticleCategory.objects.all(),
        }
        return render(request, "article/index.html", context)


class DetailView(View):
    def get(self, request, article_id):
        if request.user.is_authenticated:
            return redirect("article:login_detail")
        article = get_object_or_404(Article, pk=article_id)
        return render(request, "article/detail.html", {"article": article})

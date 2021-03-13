from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
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
            Article.objects.order_by("-publish_date")
            .filter(public=1)
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

        # ページ機能
        page = request.GET.get("page", 1)

        article_per_page = 5
        paginator = Paginator(latest_article_list, article_per_page)

        try:
            pages = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            pages = paginator.page(1)

        context = {
            "category": ArticleCategory.objects.all(),
            "pages": pages,
        }

        return render(request, "article/index.html", context)


class DetailView(View):
    def get(self, request, article_id):
        if request.user.is_authenticated:
            return redirect("article:login_detail")
        article = get_object_or_404(Article, pk=article_id)

        # 非公開の記事にアクセス
        if not article.public:
            return redirect("article:index")

        context = {
            "article": article,
            "category": ArticleCategory.objects.all(),
        }
        return render(request, "article/detail.html", context)


class CategoryView(View):
    def get(self, request, category):
        latest_article_list_filtered_by_category = (
            Article.objects.filter(category__category=category)
            .order_by("-publish_date")
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

        # ページ機能
        page = request.GET.get("page", 1)

        article_per_page = 5
        paginator = Paginator(
            latest_article_list_filtered_by_category, article_per_page
        )

        try:
            pages = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            pages = paginator.page(1)

        context = {
            "category": ArticleCategory.objects.all(),
            "filter_category": category,
            "pages": pages,
        }

        return render(request, "article/index.html", context)
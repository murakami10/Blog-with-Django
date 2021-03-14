from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView

from article.forms import AddCategoryForm
from article.forms import EmailAuthenticationForm
from article.forms import PrepareArticleForm
from article.forms import PrePostArticleForm
from article.models import Article
from article.models import ArticleCategory


class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = "article/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    pass


class Index(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        latest_article_list = (
            Article.objects.order_by("-publish_date")
            .select_related()
            .values(
                "id",
                "title",
                "author_id",
                "author__username",
                "summary",
                "publish_date",
                "public",
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
            "user": user,
            "pages": pages,
        }

        return render(request, "article/login_index.html", context)


class Detail(LoginRequiredMixin, View):
    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)
        context = {
            "article": article,
            "category": ArticleCategory.objects.all(),
            "user": user,
        }
        return render(request, "article/login_detail.html", context)


class Edit(LoginRequiredMixin, View):
    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)

        if article.author_id != user.id:
            redirect("article:index")

        form = PrePostArticleForm(instance=article)
        return render(
            request,
            "article/login_edit.html",
            {"author": user.username, "form": form},
        )

    def post(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)
        if article.author_id != user.id:
            redirect("article:index")
        form = PrePostArticleForm(request.POST, instance=article)
        if not form.is_valid():
            return render(
                request,
                "article/login_edit.html",
                {"author": user.username, "form": form},
            )
        form.save()
        messages.success(request, "更新しました")
        return redirect("article:login_index")


class Delete(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("article:login_index")
    template_name = "article/login_delete.html"

    def delete(self, request, *args, **kwargs):
        user = request.user
        article = self.get_object()
        if user.id != article.author_id:
            messages.error(self.request, "記事を削除できませんでした.")
            return redirect("article:login_index")

        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, "記事を削除しました.")

        return result


class PrepareArticle(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = PrepareArticleForm()
        return render(
            request,
            "article/prepare_post.html",
            {"author": user.username, "form": form},
        )

    def post(self, request):
        form = PrepareArticleForm(request.POST)
        user = request.user
        if not form.is_valid():
            return render(
                request,
                "article/prepare_post.html",
                {"author": user.username, "form": form},
            )

        form = PrePostArticleForm.form_with_prapare_article_data(request.POST)
        return render(
            request,
            "article/prepost_content.html",
            {"author": user.username, "form": form},
        )


class PostArticle(LoginRequiredMixin, View):
    def post(self, request):
        form = PrePostArticleForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            return render(request, "article/prepost_content.html", {"form": form})

        article = form.save(commit=False)
        article.set_author(request.user)
        form.save()
        messages.success(request, "投稿しました.")
        return redirect("article:login_index")


class CategoryView(View):
    def get(self, request, category):

        user = request.user
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
            "user": user,
            "pages": pages,
        }

        return render(request, "article/login_index.html", context)


class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):

        return render(
            request,
            "article/add_category.html",
            {"author": request.user, "form": AddCategoryForm},
        )

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "article/add_category.html",
                {"author": request.user, "form": form},
            )
        form.save()
        messages.success(request, "タグを追加しました.")
        return redirect("article:login_index")

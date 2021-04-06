from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView

from article.forms import AddCategoryForm
from article.forms import AddTagForm
from article.forms import EditArticleForm
from article.forms import EmailAuthenticationForm
from article.forms import PostArticleForm
from article.forms import PrepareArticleForm
from article.models import Article
from article.models import ArticleCategory
from article.models import Tag


class LoginView(views.LoginView):
    form_class = EmailAuthenticationForm
    template_name = "article/login/login.html"


class LogoutView(LoginRequiredMixin, views.LogoutView):
    pass


class IndexView(LoginRequiredMixin, View):

    article_per_page = 5

    def get(self, request):
        user = request.user

        latest_article_list = (
            Article.objects.order_by("-publish_date")
            .prefetch_related("tag")
            .select_related()
        )

        # ページ機能
        page = request.GET.get("page", 1)

        paginator = Paginator(latest_article_list, self.article_per_page)

        try:
            pages = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            pages = paginator.page(1)

        context = {
            "category": ArticleCategory.objects.all(),
            "tag": Tag.objects.all(),
            "user": user,
            "pages": pages,
        }

        return render(request, "article/login/index.html", context)


class DetailView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)

        next_article = (
            Article.objects.filter(
                public=1,
                publish_date__gt=article.publish_date,
                publish_date__lt=timezone.now(),
            )
            .order_by("-publish_date")
            .values("id", "title")
            .last()
        )

        pre_article = (
            Article.objects.filter(public=1, publish_date__lt=article.publish_date,)
            .order_by("-publish_date")
            .values("id", "title")
            .first()
        )

        context = {
            "article": article,
            "category": ArticleCategory.objects.all(),
            "tag": Tag.objects.all(),
            "user": user,
            "next_article": next_article,
            "pre_article": pre_article,
        }
        return render(request, "article/login/detail.html", context)


class EditView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)

        if article.author_id != user.id:
            redirect("article:index")

        form = EditArticleForm(instance=article)
        return render(
            request, "article/login/edit.html", {"author": user.username, "form": form},
        )

    def post(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)

        if article.author_id != user.id:
            redirect("article:index")

        form = EditArticleForm(request.POST, instance=article)
        if not form.is_valid():
            return render(
                request,
                "article/login/edit.html",
                {"author": user.username, "form": form},
            )

        form.save()
        messages.success(request, "更新しました")
        return redirect("article:login_index")


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("article:login_index")
    template_name = "article/login/delete.html"

    def delete(self, request, *args, **kwargs):
        user = request.user
        article = self.get_object()
        if user.id != article.author_id:
            messages.error(self.request, "記事を削除できませんでした.")
            return redirect("article:login_index")

        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, "記事を削除しました.")

        return result


class PrepareArticleView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = PrepareArticleForm()
        return render(
            request,
            "article/login/prepare_article.html",
            {"author": user.username, "form": form},
        )

    def post(self, request):
        form = PrepareArticleForm(request.POST)
        user = request.user
        if not form.is_valid():
            return render(
                request,
                "article/login/prepare_article.html",
                {"author": user.username, "form": form},
            )

        form = PostArticleForm.form_with_prapare_article_data(request.POST)
        return render(
            request,
            "article/login/post_article.html",
            {"author": user.username, "form": form},
        )


class PostArticleView(LoginRequiredMixin, View):
    def post(self, request):
        form = PostArticleForm(request.POST)
        is_valid = form.is_valid()
        if not is_valid:
            return render(request, "article/login/post_article.html", {"form": form})

        article = form.save(commit=False)
        article.set_author(request.user)
        form.save()
        messages.success(request, "投稿しました.")
        return redirect("article:login_index")


class CategoryView(LoginRequiredMixin, View):

    article_per_page = 5

    def get(self, request, category):

        user = request.user
        latest_article_list_filtered_by_category = (
            Article.objects.filter(category__name=category)
            .order_by("-publish_date")
            .prefetch_related("tag")
            .select_related()
        )

        # ページ機能
        page = request.GET.get("page", 1)

        paginator = Paginator(
            latest_article_list_filtered_by_category, self.article_per_page
        )

        try:
            pages = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            pages = paginator.page(1)

        context = {
            "category": ArticleCategory.objects.all(),
            "tag": Tag.objects.all(),
            "filter_category": category,
            "user": user,
            "pages": pages,
        }

        return render(request, "article/login/index.html", context)


class TagView(LoginRequiredMixin, View):

    article_per_page = 5

    def get(self, request, tag):
        user = request.user
        latest_article_list_filtered_with_tag = (
            Article.objects.filter(tag__name=tag)
            .order_by("-publish_date")
            .prefetch_related("tag")
            .select_related()
        )

        # ページ機能
        page = request.GET.get("page", 1)

        paginator = Paginator(
            latest_article_list_filtered_with_tag, self.article_per_page
        )

        try:
            pages = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            pages = paginator.page(1)

        context = {
            "category": ArticleCategory.objects.all(),
            "tag": Tag.objects.all(),
            "filter_tag": tag,
            "user": user,
            "pages": pages,
        }

        return render(request, "article/login/index.html", context)


class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):

        return render(
            request,
            "article/login/add_tag_category.html",
            {
                "author": request.user,
                "form_category": AddCategoryForm,
                "form_tag": AddTagForm,
                "category": ArticleCategory.objects.all(),
                "tag": Tag.objects.all(),
            },
        )

    def post(self, request):
        form = AddCategoryForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "article/login/add_tag_category.html",
                {
                    "author": request.user,
                    "form_category": form,
                    "form_tag": AddTagForm,
                    "category": ArticleCategory.objects.all(),
                    "tag": Tag.objects.all(),
                },
            )
        form.save()
        messages.success(request, "カテゴリを追加しました.")
        return redirect("article:login_index")


class AddTagView(LoginRequiredMixin, View):
    def post(self, request):
        form = AddTagForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                "article/login/add_tag_category.html",
                {"author": request.user, "form_category": form, "form_tag": form},
            )
        form.save()
        messages.success(request, "タグを追加しました.")
        return redirect("article:login_index")

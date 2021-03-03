from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import View

from .forms import EmailAuthenticationForm
from .forms import PrepareArticleForm
from .forms import PrePostArticleForm
from .models import Article


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
        context = {"latest_article_list": latest_article_list}
        return render(request, "article/index.html", context)


class DetailView(View):
    def get(self, request, article_id):
        if request.user.is_authenticated:
            return redirect("article:login_detail")
        article = get_object_or_404(Article, pk=article_id)
        return render(request, "article/detail.html", {"article": article})


class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = "article/login.html"


class Logout(LoginRequiredMixin, LogoutView):
    pass


class LoginIndex(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
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
        content = {"latest_article_list": latest_article_list, "user": user}
        return render(request, "article/login_index.html", content)


class LoginDetail(LoginRequiredMixin, View):
    def get(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, pk=article_id)
        return render(
            request, "article/login_detail.html", {"article": article, "user": user}
        )


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
        return redirect("article:index")

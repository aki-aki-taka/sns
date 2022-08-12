from django.shortcuts import render
from django.shortcuts import redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.views import generic


from .models import Post, Category, Connection


class TopView(TemplateView):
    template_name = 'base/top.html'


class Home(LoginRequiredMixin, ListView):
    """HOMEページで、自分以外のユーザー投稿をリスト表示"""
    model = Post
    template_name = 'base/list.html'

    def get_queryset(self):
        # リクエストユーザーのみ除外
        return Post.objects.exclude(user=self.request.user)

        def get_context_data(self, *args, **kwargs):
            context = super().get_context_data(*args, **kwargs)
            # get_or_createにしないとサインアップ時オブジェクトがないためエラーになる
            context['connection'] = Connection.objects.get_or_create(user=self.request.user)
            return context


class MyPost(LoginRequiredMixin, ListView):
    """自分の投稿のみ表示"""
    model = Post
    template_name = 'base/mylist.html'

    def get_queryset(self):
        # 自分の投稿に限定
        return Post.objects.filter(user=self.request.user)


class DetailPost(LoginRequiredMixin, DetailView):
    """投稿詳細ページ"""
    model = Post
    template_name = 'base/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context


class CreatePost(LoginRequiredMixin, CreateView):
    """投稿フォーム"""
    model = Post
    template_name = 'base/create.html'
    fields = ['title', 'content', 'image', 'category']
    success_url = reverse_lazy('base:top')

    def form_valid(self, form):
        """投稿ユーザーをリクエストユーザーと紐付け"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """投稿編集ページ"""
    model = Post
    template_name = 'base/update.html'
    fields = ['title', 'content', 'image', 'category']

    def get_success_url(self,  **kwargs):
        """編集完了後の遷移先"""
        pk = self.kwargs["pk"]
        return reverse_lazy('base:detail', kwargs={"pk": pk})

    def test_func(self, **kwargs):
        """アクセスできるユーザーを制限"""
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """投稿編集ページ"""
    model = Post
    template_name = 'base/delete.html'
    success_url = reverse_lazy('base:top')

    def test_func(self, **kwargs):
        """アクセスできるユーザーを制限"""
        pk = self.kwargs["pk"]
        post = Post.objects.get(pk=pk)
        return (post.user == self.request.user)


""" カテゴリー一覧 """


class CategoryView(generic.ListView):
    model = Post
    template_name = 'base/list.html'

    def get_queryset(self):
        category = Category.objects.get(name=self.kwargs['category'])
        queryset = Post.objects.order_by('-id').filter(category=category)
        return queryset

    """ アクセスされた値を取得し辞書に格納 """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_key'] = self.kwargs['category']
        return context

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # get_or_createにしないとサインアップ時オブジェクトがないためエラーになる
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context



class FollowBase(LoginRequiredMixin, View):
    """フォローのベース。リダイレクト先を以降で継承先で設定"""
    def get(self, request, *args, **kwargs):
        # ユーザーの特定
        pk = self.kwargs['pk']
        target_user = Post.objects.get(pk=pk).user

        # ユーザー情報よりコネクション情報を取得。存在しなければ作成
        my_connection = Connection.objects.get_or_create(user=self.request.user)

    # フォローテーブル内にすでにユーザーが存在する場合
        if target_user in my_connection[0].following.all():
        # テーブルからユーザーを削除
            obj = my_connection[0].following.remove(target_user)
        # フォローテーブル内にすでにユーザーが存在しない場合
        else:
            # テーブルにユーザーを追加
            obj = my_connection[0].following.add(target_user)
        return obj


class FollowHome(FollowBase):
    """HOMEページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        # FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        # homeにリダイレクト
        return redirect('base:home')


class FollowDetail(FollowBase):
    """詳細ページでフォローした場合"""
    def get(self, request, *args, **kwargs):
        # FollowBaseでリターンしたobj情報を継承
        super().get(request, *args, **kwargs)
        pk = self.kwargs['pk']
        # detailにリダイレクト
        return redirect('base:detail', pk)


class FollowList(LoginRequiredMixin, ListView):
    """フォローしたユーザーの投稿をリスト表示"""
    model = Post
    template_name = 'base/list.html'

    def get_queryset(self):
        """フォローリスト内にユーザーが含まれている場合のみクエリセット返す"""
        my_connection = Connection.objects.get_or_create(user=self.request.user)
        all_follow = my_connection[0].following.all()
        # 投稿ユーザーがフォローしているユーザーに含まれている場合オブジェクトを返す。
        return Post.objects.filter(user__in=all_follow)


    def get_context_data(self, *args, **kwargs):
        """コネクションに関するオブジェクト情報をコンテクストに追加"""
        context = super().get_context_data(*args, **kwargs)
        # コンテクストに追加
        context['connection'] = Connection.objects.get_or_create(user=self.request.user)
        return context

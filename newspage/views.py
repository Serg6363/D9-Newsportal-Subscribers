from urllib import request

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from django.core.paginator import Paginator

from .models import Post, Category, User
from .filters import PostFilter
import datetime
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 20


class PostText(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.time()
        context['value1'] = None
        context['user_auth'] = self.request.user.is_authenticated
        id = self.kwargs.get('pk')
        post = Post.objects.get(pk=id)
        is_subscriber = True
        for category in post.post_category.all():
            if self.request.user not in category.user_subscriber.all():
                is_subscriber = False
        context['is_subscriber'] = is_subscriber
        context['post_category'] = context['post'].post_category
        return context


class PostSearch(ListView):
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'post_search'
    queryset = Post.objects.order_by('-id')
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('newspage.add_post',)
    template_name = 'post_add.html'
    form_class = PostForm
    success_url = '/news/'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('newspage.update_post',)
    template_name = 'post_edit.html'
    form_class = PostForm
    success_url = '/news/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class SubscriptionsList(ListView):
    model = Post
    template_name = 'subscriptions.html'
    context_object_name = 'subscriptions'
    queryset = Post.objects.all()


class CategoryText(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'cat'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(CategoryText, self).get_context_data(**kwargs)
        context['cat'] = Category.objects.get(id=id)
        return context

@login_required
def subscribe_categories(request, pk):
    user = User.objects.get(pk=request.user.id)
    # получаю ID пользователя, присваиваю переменно user
    post = Post.objects.get(pk=pk)
    # получаю
    categories = post.post_category.all()
    for category in categories:
        if user not in category.user_subscriber.all():
            category.user_subscriber.add(user)
    return redirect('/news')


@login_required
def unsubscribe_categories(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    for category in categories:
        if user in category.user_subscriber.all():
            category.user_subscriber.remove(user)
    return redirect('/news')

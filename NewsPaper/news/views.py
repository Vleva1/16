from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.views import View

from .filters import PostFilter

from .models import Author, Category, Posts, Comment

from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from datetime import datetime

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

class AuthorsList(ListView):
    model = Author
    ordering = 'name'
    template_name = 'auth.html'
    context_object_name = 'authors'

class CategorysList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categorys.html'
    context_object_name = 'categorys'

class PostsList(ListView):
    model = Posts
    ordering = 'dt_of_publication'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
class CommentsList(ListView):
    model = Comment
    ordering = 'posts'
    template_name = 'comments.html'
    context_object_name = 'comments'

class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Posts
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'



class PostCreate(CreateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Posts
    template_name = 'post_create.html'



    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            path_info = self.request.META['PATH_INFO']
            if path_info == '/news/create/':
                post.post_type = 'NE'
            elif path_info == '/articles/create/':
                post.post_type = 'AR'
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView, PermissionRequiredMixin):
    form_class = PostForm
    model = Posts
    template_name = 'post_edit.html'
    permission_required = ('posts.change_post')



class PostDelete(DeleteView, PermissionRequiredMixin):
    model = Posts
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_')
    permission_required = ('posts.delete_post')


class PostSearch(ListView):
    model = Posts
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = '-dt_of_publication'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
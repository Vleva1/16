from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import  PermissionRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .filters import PostFilter

from .models import Author, Category, Posts, Comment, Appointment

from .forms import PostForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView

from datetime import datetime
from django.http import HttpResponse
from django.views import View
from .tasks import hello, printer, send_email, last_post_week


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')



class IndexView(View):
    def get(self, request):
        printer.delay(10)
        hello.delay()
        return HttpResponse('Hello!')

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


class AppointmentView(View):
    template_name = 'appointment_created.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'appointment_created.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            user_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # отправляем письмо
        send_email()
        last_post_week()
@login_required
def subscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Posts.objects.get(pk=pk)
    category = post.category.all()
    for cat in category:
        if user not in cat.subscribers.all():
            cat.subscribers.add(user)
    message = "доне"
    return render(request, 'subscribe.html', {"category": category, 'message': message})

@login_required
def unsubscribe(request, pk):
    user = User.objects.get(pk=request.user.id)
    post = Posts.objects.get(pk=pk)
    category = post.name_category.all()
    for cat in category:
        if user in cat.subscribers.all():
            cat.subscribers.remove(user)
    message = "доне"
    return render(request, 'unsubscribe.html',{"category" : category, 'message' : message })


class CategoryListView(ListView):
     model = Posts
     template_name = 'category_list.html'
     context_object_name = 'category_news_list'

     def get_queryset(self):
         self.category = get_object_or_404(Category, id = self.kwargs['pk'])
         queryset = Posts.objects.filter(category = self.category).order_by('-category')
         return queryset

     def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
         context['category'] = self.category
         return context
from allauth.account.views import LogoutView
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.views.decorators.cache import cache_page

from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, subscribe, CategoryListView, \
   IndexView

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', cache_page(60*10)(PostsList.as_view()), name = 'posts_'),
   path('<int:pk>', cache_page(60*10)(PostDetail.as_view()), name = 'post_detail'),
   path('create/', PostCreate.as_view(), name='create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='delete'),
   path('search/', PostSearch.as_view(), name='search'),
   path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
   path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
   path('subscribe/<int:pk>', subscribe, name='subscribe'),
   path('unsubscribe/<int:pk>', subscribe, name='unsubscribe'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   #path('', IndexView.as_view()),
]

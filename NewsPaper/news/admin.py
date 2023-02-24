from django.contrib import admin
from .models import Author, Category, Posts, Comment, PostCategory


class PostsAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('title', 'dt_of_publication')  # генерируем список имён всех полей для более красивого отображения


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Comment)
admin.site.register(PostCategory)

# Register your models here.

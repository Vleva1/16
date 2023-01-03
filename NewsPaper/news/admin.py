from django.contrib import admin
from .models import Author, Category, Posts, Comment, PostCategory

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Posts)
admin.site.register(Comment)
admin.site.register(PostCategory)

# Register your models here.

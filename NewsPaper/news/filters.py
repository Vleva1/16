from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Posts, Author, Category
from django import forms

class PostFilter(FilterSet):
     date_create__gt = DateFilter(field_name='dt_of_publication', label='Start date', widget=forms.DateInput(
         attrs = {'type': 'date'}),lookup_expr = 'date__gte')
     class Meta:
        model = Posts
        fields = {
            'title': ['icontains'],
            'author': ['exact'], }

        search_title = CharFilter(
            field_name = 'title',
            label = 'Название статьи',
            lookup_expr = 'icontains'
        )
        search_author = ModelChoiceFilter(
            empty_label = 'Все авторы',
            field_name = 'authors',
            label = 'Автор',
            queryset = Author.objects.all()
        )
        post_dt_of_publication = DateFilter(
            field_name = 'dt_of_publication',
            widget = forms.DateInput(attrs = {'type': 'date'}),
            label = 'Дата',
            lookup_expr = 'date__gte'
        )

class CategFilter(FilterSet):
   class Meta:
       model = Category
       fields = {

           'name': ['icontains'],
       }
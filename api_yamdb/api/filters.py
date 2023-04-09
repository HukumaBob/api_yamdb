from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']

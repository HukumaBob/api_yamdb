from django_filters import CharFilter
from django_filters.rest_framework import FilterSet
from reviews.models import Title


class TitleFilter(FilterSet):
    """
    Custom filter class for filtering Title objects.
    Inherits from Django FilterSet.
    """

    # Filter for category slug
    category = CharFilter(field_name='category__slug')

    # Filter for genre slug
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'name', 'year']

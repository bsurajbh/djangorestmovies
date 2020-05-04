from django_filters import rest_framework as filters
from api.movies.models import Movies


class MoviesFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter(lookup_expr='exact')

    class Meta:
        model = Movies
        fields = ['name', 'year']

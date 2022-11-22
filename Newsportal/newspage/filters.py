import django_filters
from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    time_filter = django_filters.DateFilter(field_name='time_write', lookup_expr='gt', label='Опубликовано после')

    class Meta:
        model = Post
        fields = ['time_filter', 'author']

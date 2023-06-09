import django_filters
from django_filters import DateFilter , CharFilter
from .models import Post

class PostsFilter(django_filters.FilterSet):
    startDate = DateFilter(field_name='publishDate',lookup_expr='gte')
    endDate = DateFilter(field_name='publishDate',lookup_expr='lte')
    text = CharFilter(field_name='text', lookup_expr='icontains')
    
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['image','lastModified','dislikes']
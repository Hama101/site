import django_filters as f
from django_filters import CharFilter

from .models import *


class PostFilter(f.FilterSet):
    title = CharFilter(field_name='title' , lookup_expr='icontains' , label="" , )
    pays = CharFilter(field_name='pays' , lookup_expr='icontains', label="")
    ville = CharFilter(field_name='ville' , lookup_expr='icontains', label="")
    class Meta:
        model = Post
        fields = ['category','sub_category','title' , 'pays' ,'ville','sub_sub']


class BlogFilter(f.FilterSet):
    class Meta:
        model = Blog
        fields = ['tags']
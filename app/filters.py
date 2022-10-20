
import django_filters
from .models import *


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'text':['icontains'],
            'user__profile__name':['icontains'],
        }
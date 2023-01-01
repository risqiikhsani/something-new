
import django_filters
from .models import *


# WORKS !
class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            'text':['contains'],
            'user__profile__name':['contains'],
        }

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UserList, UserDetail

restricted_urlpatterns = [
    path('restricted/users',UserList.as_view(), name='r-user-list'),
    path('restricted/user/<int:id>',UserDetail.as_view(), name='r-user-detail'),
]

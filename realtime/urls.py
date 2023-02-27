from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (
    NotificationList
)

urlpatterns = [

    path('notifications',NotificationList.as_view(), name='notification-list'),

]
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views_auth import(
    Register,
    Login,
    ChangePassword,
)

from .views import (
    api_root,
    UserList,
    UserDetail,
)   


urlpatterns = [
    path('register/',Register.as_view(), name='register'),
    path('login/',Login.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('', api_root),
    path('user-list/',UserList.as_view(), name='user-list'),
    path('user-detail/',UserDetail.as_view(), name="user-detail"),
]
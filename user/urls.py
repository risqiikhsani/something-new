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

    ConnectionViewSet,
    RequestViewSet,
)   




urlpatterns = [
    path('register/',Register.as_view(), name='register'),
    path('login/',Login.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
    path('', api_root),
    path('user-list/',UserList.as_view(), name='user-list'),
    path('user-detail/',UserDetail.as_view(), name="user-detail"),

    path('connections/',ConnectionViewSet.as_view({'get':'list'}), name='connection-list'),
    path('user/<int:pk>/connections/',ConnectionViewSet.as_view({'get':'user_connection_list'}), name='user-connection-list'),
    path('connections/<int:pk>/block/',ConnectionViewSet.as_view({'get':'block_connection'}), name='connection-detail-block'),

    path('requests/',RequestViewSet.as_view({'get':'list'}), name='request-list'),
    path('user/<int:user_id>/send_request/',RequestViewSet.as_view({'get':'send_request'}),name='send-request'),
    path('user/<int:user_id>/cancel_sent_request/',RequestViewSet.as_view({'get':'cancel_sent_request'}),name='cancel-sent-request'),
    path('requests/<int:pk>/accept/',RequestViewSet.as_view({'get':'accept_request'}),name='accept-request'),
    path('requests/<int:pk>/decline/',RequestViewSet.as_view({'get':'decline_request'}),name='decline-request'),

]
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .staff_rest.urls import restricted_urlpatterns
from .views import (ConnectionViewSet, RequestViewSet, UserDetail, UserList,
                    UserViewSet, api_root, MyProfile, MyUser,
                    UserRelationship)
from .views_auth import (ChangePassword, EmailVerification, ForgotPassword,
                         ForgotPasswordCheckOptional, ForgotPasswordConfirm,
                         Login, Register, SendEmailVerification)
from .views_auth2 import GoogleLoginApi

# from .views_auth2 import (
#     FacebookLogin,
#     GithubLogin,
#     GoogleLogin,
# )






urlpatterns = restricted_urlpatterns + [
    path('', api_root),
    path('user-list',UserList.as_view(), name='user-list'),
    path('user-detail/<int:pk>',UserDetail.as_view(), name="user-detail"),

    path('my/user',MyUser.as_view(), name='my-user'),
    path('my/profile',MyProfile.as_view(), name='my-profile'),

    # WORKS
    path('connections',ConnectionViewSet.as_view({'get':'list'}), name='connection-list'),
    # WORKS
    path('user/<int:pk>/connections',UserViewSet.as_view({'get':'user_connection_list'}), name='user-connection-list'),
    # WORKS (get,put)
    path('user/<int:pk>/relationship',UserRelationship.as_view(), name='user-relationship'),
    # WORKS
    #path('connections/<int:pk>/remove',ConnectionViewSet.as_view({'get':'remove_connection'}), name='connection-detail-remove'),
    path('user/<int:pk>/remove_connection',UserViewSet.as_view({'get':'remove_connection'}), name='connection-remove'),

    # WORKS
    path('requests',RequestViewSet.as_view({'get':'list'}), name='request-list'),
    # WORKS
    path('my/waiting-requests',RequestViewSet.as_view({'get':'waiting_requests'}), name='waiting-request-list'),
    # WORKS
    path('user/<int:pk>/send_request',UserViewSet.as_view({'get':'send_request'}),name='send-request'),
    # WORKS
    path('user/<int:pk>/cancel_sent_request',UserViewSet.as_view({'get':'cancel_sent_request'}),name='cancel-sent-request'),
    # WORKS
    path('requests/<int:pk>/accept',RequestViewSet.as_view({'get':'accept_request'}),name='accept-request'),
    # WORKS
    path('requests/<int:pk>/decline',RequestViewSet.as_view({'get':'decline_request'}),name='decline-request'),

]

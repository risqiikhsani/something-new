from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views_auth import(
    Register,
    Login,
    ChangePassword,
    SendEmailVerification,
    EmailVerification,
)

from .views_auth2 import (
    GoogleLoginApi,
)

# from .views_auth2 import (
#     FacebookLogin,
#     GithubLogin,
#     GoogleLogin,
# )

from .views import (
    api_root,
    UserList,
    UserDetail,

    ConnectionViewSet,
    RequestViewSet,
    UserViewSet,
    my_user,
    my_profile,
    user_relationship,
)   




urlpatterns = [
    path('register',Register.as_view(), name='register'),
    path('login',Login.as_view(), name='login'),
    path('login/google',GoogleLoginApi.as_view(), name='login-google'),
    path('token-refresh', TokenRefreshView.as_view(), name='refresh-token'),
    path('change-password', ChangePassword.as_view(), name='change-password'),
    path('send-email-verification',SendEmailVerification.as_view(),name="send-email-verification"),
    path('email-verification/<str:uuid>',EmailVerification.as_view(),name="email-verification"),
    

    # path('dj-rest-auth/', include('dj_rest_auth.urls')), 
    # path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('dj-rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),    
    # path('dj-rest-auth/github/', GithubLogin.as_view(), name='github_login'),
    # path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),

    path('', api_root),
    path('user-list',UserList.as_view(), name='user-list'),
    path('user-detail/<int:pk>',UserDetail.as_view(), name="user-detail"),

    path('my/user',my_user.as_view(), name='my-user'),
    path('my/profile',my_profile.as_view(), name='my-profile'),

    # WORKS
    path('connections',ConnectionViewSet.as_view({'get':'list'}), name='connection-list'),
    # WORKS
    path('user/<int:pk>/connections',UserViewSet.as_view({'get':'user_connection_list'}), name='user-connection-list'),
    # WORKS (get,put)
    path('user/<int:pk>/relationship',user_relationship.as_view(), name='user-relationship'),
    # WORKS
    #path('connections/<int:pk>/remove',ConnectionViewSet.as_view({'get':'remove_connection'}), name='connection-detail-remove'),

    path('user/<int:pk>/remove_connection',UserViewSet.as_view({'get':'remove_connection'}), name='connection-remove'),


    # WORKS
    path('requests',RequestViewSet.as_view({'get':'list'}), name='request-list'),
    # WORKS
    path('waiting-requests',RequestViewSet.as_view({'get':'waiting_requests'}), name='waiting-request-list'),
    # WORKS
    path('user/<int:pk>/send_request',UserViewSet.as_view({'get':'send_request'}),name='send-request'),
    # WORKS
    path('user/<int:pk>/cancel_sent_request',UserViewSet.as_view({'get':'cancel_sent_request'}),name='cancel-sent-request'),
    # WORKS
    path('requests/<int:pk>/accept',RequestViewSet.as_view({'get':'accept_request'}),name='accept-request'),
    # WORKS
    path('requests/<int:pk>/decline',RequestViewSet.as_view({'get':'decline_request'}),name='decline-request'),

]
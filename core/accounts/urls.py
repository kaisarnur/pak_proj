from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    RegisterView, LoginApiView, LogoutAPIView, UserDetailView, DeleteAccountView, ProfileViewSet
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('delete_user/', DeleteAccountView.as_view(), name='delete_user'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', ProfileViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

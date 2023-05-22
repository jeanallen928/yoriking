from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.Signupview.as_view(), name='signup'),
    path('mypage/', views.UserDetailView.as_view(), name='mypage_view'),
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
]
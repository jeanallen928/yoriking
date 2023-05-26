from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.urls import path

urlpatterns = [
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('<int:user_id>/follow/', views.FollowView.as_view(), name='follow_view'),    
    path('kakao/login/', views.KakaoLoginView.as_view(), name='kakao_login'),
]


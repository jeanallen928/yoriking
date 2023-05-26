from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from . import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('mypage/', views.MypageView.as_view(), name='mypage'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('<int:user_id>/follow/', views.FollowView.as_view(), name='follow_view'),    
    path('kakao/login/', views.KakaoLoginView.as_view(), name='kakao_login'),
]


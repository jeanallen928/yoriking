from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.generics import get_object_or_404
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
from . models import User
import requests


class MypageView(APIView):
    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)


class UserView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user.is_active == True:
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        else :
            return Response({"message":"탈퇴한 회원입니다."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, user_id):
        if user_id != request.user.id:
            return Response({"message":"본인의 프로필만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"프로필 수정 완료!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        if user_id != request.user.id:
            return Response({"message":"본인의 프로필만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        user = request.user
        user.is_active = False
        user.save()
        return Response({"message": "회원 탈퇴 완료!"}, status=status.HTTP_200_OK)


class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if you.id == me.id:
            return Response({"message": "본인을 팔로우 할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        if me in you.followers.all():
            you.followers.remove(me)
            return Response({"message":"언팔로우"}, status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response({"message":"팔로우"}, status=status.HTTP_200_OK)


class KakaoLoginView(APIView):
    def post(self, request):
        try:
            access_token = request.data["access_token"]
            account_info = requests.get(
                "https://kapi.kakao.com/v2/user/me", headers={"Authorization":f"Bearer {access_token}"}).json()
            email = account_info["kakao_account"]["email"]
            profile_image = account_info["properties"]["profile_image"]

            if User.objects.filter(email=email).exists():
                account = User.objects.get(email=email)
            else:
                nickname = account_info["properties"]["nickname"]
                unique_nickname = generate_unique_nickname(nickname)
                account = User.objects.create(email=email, nickname=unique_nickname, image=profile_image)

            token = CustomTokenObtainPairSerializer.get_token(account)
            access = str(token.access_token)
            refresh = str(token)

            return Response(
                {
                    "refresh":refresh,
                    "access":access,
                },
                status=status.HTTP_200_OK
            )

        except KeyError:
            return Response({"message":"Key Error"})


def generate_unique_nickname(nickname):
    base_nickname = nickname
    suffix = 1
    while User.objects.filter(nickname=nickname).exists():
        suffix += 1
        nickname = f"{base_nickname}_{suffix}"
    return nickname


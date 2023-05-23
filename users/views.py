from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.generics import get_object_or_404
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer
from . models import User


class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


class MypageView(APIView):
    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)


class UserView(APIView):  
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
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
        user.delete()
        return Response({"message": "회원 탈퇴 완료!"}, status=status.HTTP_200_OK)
    

class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        user.save()
        return Response("get 요청")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all():
            you.followers.remove(me)
            return Response({"언팔로우"}, status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response({"팔로우"}, status=status.HTTP_200_OK)
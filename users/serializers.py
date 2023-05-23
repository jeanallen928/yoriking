from rest_framework import serializers
from users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.save()
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True, read_only = True)
    followings = serializers.StringRelatedField(many=True, read_only = True)
    # article_set = ArticleListSerializer(many=True)
    # like_articles = ArticleListSerializer(many=True)

    class Meta:
        model = User
        fields = ("nickname", "bio", "followings", "followers") # "article"
        
    
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # password = validated_data.get('password')
        # user.set_password(password)
        user.save()
        return user
    
     
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nickname'] = user.nickname

        return token
from rest_framework import serializers
from users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()  
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "email",
            "password",
            "bio",
            "image",
            "article_count",
            "following_count",
            "follower_count",
            "followings",
            "followers",
            "articles"
            )
        extra_kwargs = {
            "password":{'write_only':True},
        }
        

    def get_followers(self, obj):
        followers_data = obj.followers.values('id', 'nickname', 'image', 'email')
        return followers_data
    
    def get_followings(self, obj):
        followings_data = obj.followings.values('id', 'nickname', 'image', 'email')
        return followings_data
    
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.followings.count()
    
    def get_article_count(self, obj):
        return obj.articles.count()

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nickname'] = user.nickname

        return token
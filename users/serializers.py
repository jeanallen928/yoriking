from rest_framework import serializers
from users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data.get('password')
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    followings = serializers.SerializerMethodField()    
    articles = serializers.SerializerMethodField()
    
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "nickname",
            "email",
            "bio",
            "image",
            "preference",
            "article_count",
            "following_count",
            "follower_count",
            "followings",
            "followers",
            "articles"
            )

    def get_followers(self, obj):
        followers_data = obj.followers.values('id', 'nickname', 'image')
        return followers_data
    
    def get_followings(self, obj):
        followings_data = obj.followings.values('id', 'nickname', 'image')
        return followings_data
    
    def get_articles(self, obj):
        articles = obj.articles.all()
        article_data = ArticleSerializer(articles, many=True).data
        for article in article_data:
            article.pop('likes', None)
            article.pop('content', None)
        return article_data
    
    def get_follower_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.followings.count()
    
    def get_article_count(self, obj):
        return obj.articles.count()

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        user.save()
        return user
    
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['nickname'] = user.nickname

        return token
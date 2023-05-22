from rest_framework import serializers
from articles.models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Comment
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(article=obj).count()

    def get_like_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.nickname
    
    def get_comment_count(self, obj):
        return Comment.objects.filter(article=obj).count()

    def get_like_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Article
        fields = "__all__"

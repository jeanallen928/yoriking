from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from articles.models import Article, Comment
from articles.serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)


# articles/
class ArticleView(APIView):
    """
    게시글 전체 목록 조회
    """

    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 작성
    """

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


# articles/<int:article_id>/
class ArticleDetailView(APIView):
    """
    게시글 상세보기
    """

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    게시글 수정하기
    """

    def put(self, request, article_id):
        pass

    """
    게시글 삭제하기
    """

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# articles/<int:article_id>/comments/
class CommentView(APIView):
    """
    댓글 조회
    """

    def get(self, request):
        pass

    """
    댓글 작성
    """

    def post(self, request):
        pass


# articles/comments/<int:comment_id>/
class CommentDetailView(APIView):
    """
    댓글 수정
    """

    def put(self, request, comment_id):
        pass

    """
    댓글 삭제
    """

    def delete(self, request, comment_id):
        pass


# articles/<int:article_id>/like/
class LikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    """
    게시글 좋아요
    """

    def post(self, request, article_id):
        pass
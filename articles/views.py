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
    # 로그인한 사람은 작성 가능. 아니면 읽기만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        return Response(({"message": "게시글 작성 완료!"}, serializer.data), status=status.HTTP_200_OK)


# articles/<int:article_id>/
class ArticleDetailView(APIView):
    # 로그인한 사람은 수정/삭제 가능. 아니면 읽기만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article, data=request.data)
        if article.user == request.user:
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(({"message": "게시글 수정 완료!"},serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    """
    게시글 삭제하기
    """

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if article.user == request.user:
            article.delete()
            return Response({"message": "게시글 삭제 완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# articles/<int:article_id>/comments/
class CommentView(APIView):
    # 로그인한 사람은 작성 가능. 아니면 조회만 가능.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
    # 로그인한 사람만 수정/삭제 가능
    permission_classes = [permissions.IsAuthenticated]
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
    # 로그인한 사람만 좋아요 가능
    permission_classes = [permissions.IsAuthenticated]
    """
    게시글 좋아요
    """

    def post(self, request, article_id):
        article = get_object_or_404(Article, id = article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response({"massage":"좋아요 취소"}, status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response({"massage":"좋아요"}, status=status.HTTP_200_OK)
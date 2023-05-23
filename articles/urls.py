from django.urls import path
from articles import views

urlpatterns = [
    path("", views.ArticleView.as_view(), name="article-view"),
    path("<int:article_id>/", views.ArticleDetailView.as_view(), name="article-detail-view"),
    path("<int:article_id>/comments/", views.CommentView.as_view(), name="comment-view"),
    path("comments/<int:comment_id>/", views.CommentDetailView.as_view(), name="comment-detail-view"),
    path("<int:article_id>/like/", views.LikeView.as_view(), name="like-view"),
    path('pagination/', views.ArticlesPaginationViewSet.as_view({'get': 'list'}), name='article-pagination'),
]

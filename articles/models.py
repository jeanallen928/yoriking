from django.db import models
from users.models import User


class Category(models.Model):
    CATEGORIES = (
        ('KOR', '한식'),
        ('CHN', '중식'),
        ('JPN', '일식'),
        ('WES', '양식'),
        ('ETC', '그외'),
    )
    
    category = models.CharField("카테고리", choices=CATEGORIES, max_length=3)
    
    def __str__(self):
        return self.category
    

class Article(models.Model):
    
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    image = models.ImageField("이미지", upload_to="article/%Y/%m/", blank=True)
    likes = models.ManyToManyField(User, verbose_name="좋아요", blank=True, related_name='like_articles')
    category = models.ForeignKey(Category, verbose_name="카테고리", related_name="categorized_articles")

    class Meta:
        def __str__(self):
            return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("댓글 생성일", auto_now_add=True)
    updated_at = models.DateTimeField("댓글 수정일", auto_now=True)
    

    class Meta:
        def __str__(self):
            return self.content

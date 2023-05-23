from django.db import models
from users.models import User


class Article(models.Model):
    CATEGORIES = (
        ('KO', '한식'),
        ('CH', '중식'),
        ('JP', '일식'),
        ('WE', '양식'),
        ('ET', '그외'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    created_at = models.DateTimeField("생성일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    image = models.ImageField("이미지", null=True, upload_to="", blank=True)
    like = models.ManyToManyField(User, blank=True, related_name='likes')
    category = models.CharField("카테고리", choices=CATEGORIES, max_length=10)

    class Meta:
        def __str__(self):
            return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField("댓글 내용")
    created_at = models.DateTimeField("댓글 생성일", auto_now_add=True)
    updated_at = models.DateTimeField("댓글 수정일", auto_now=True)
    

    class Meta:
        def __str__(self):
            return self.content

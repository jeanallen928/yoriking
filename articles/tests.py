from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# 이미지
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile, random

from faker import Faker

from users.models import User
from articles.models import Article, Comment
from articles.serializers import ArticleDetailSerializer, ArticleSerializer


def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


# view = ArticleView, url name = "article_view", method = post
class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.article_data = {"title": "test Title", "content": "test content"}
        cls.user = User.objects.create_user("test@test.com", "Test1234!")

    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]

    # 테스트 후 이미지 파일 삭제하기
    def tearDown(self):
        for article in Article.objects.all():
            article.image.delete()
            article.delete()

    # 게시글 작성 성공(NOT NULL(title, content))
    def test_pass_create_article(self):
        response = self.client.post(
            path=reverse("article_view"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data[0]["message"], "게시글 작성 완료!")
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, "test Title")


    # 이미지가 있는 게시글 작성 성공
    def test_pass_create_article_with_image(self):
        
        temp_file = tempfile.NamedTemporaryFile()  # 임시 파일 생성
        temp_file.name = "image.png"  # 임시 파일 이름 지정
        image_file = get_temporary_image(temp_file)  # 맨 위의 함수에 넣어서 이미지 파일을 받아온다.
        image_file.seek(0)  # 이미지의 첫번째 프레임을 받아온다. 그냥 파일이기 때문에 첫번째 프레임을 받아오는 과정 필요.
        
        self.article_data["image"] = image_file
        
        response = self.client.post(
            path=reverse("article_view"),
            data=encode_multipart(data=self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.get().title, "test Title")
      
      
    # 로그인 안 했을 때 게시글 작성 실패
    def test_fail_create_article_if_not_logged_in(self):
        url = reverse("article_view")
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)


class ArticleReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.user = User.objects.create(
                email=cls.faker.unique.email(), 
                password=cls.faker.word(), 
                nickname=cls.faker.unique.name()
                )
            cls.articles.append(Article.objects.create(
                title=cls.faker.sentence(), 
                content=cls.faker.text(), 
                user=cls.user
                ))


    # 게시글 전체 목록 조회 성공
    # view = ArticleView, url name = "article_view", method = get
    def test_pass_article_list(self):
        response = self.client.get(path=reverse("article_view"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # 게시글 상세 보기(10개 테스트) 성공
    # view = ArticleDetailView, url name = "article_detail_view", method = get
    def test_pass_article_detail(self):
        for article in self.articles:
            url = article.get_absolute_url()
            response = self.client.get(url)
            serializer = ArticleDetailSerializer(article).data
            for key, value in serializer.items():
                self.assertEqual(response.data[key], value)


# view = ArticleDetailView, url name = "article_detail_view", method = put
class ArticleUpdateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.user = User.objects.create(email="test@test.com", password="Test1234!", nickname="test")
        cls.user.set_password(cls.user_data["password"])
        cls.user.save()
        
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.articles.append(Article.objects.create(
                title=cls.faker.word(), 
                content=cls.faker.text(),
                user=cls.user
                ))
        
        cls.new_articles=[]
        for i in range(10):
            cls.new_articles.append({
                "title": cls.faker.word(), 
                "content": cls.faker.text(),
                })

    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]    
    
    # 게시글 수정 성공(NOT NULL(title, content))
    def test_pass_update_article(self):
        for i in range(10):
            url = self.articles[i].get_absolute_url()
            response = self.client.put(
                path=url, 
                data=self.new_articles[i],
                HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                )
            
            # 게시글 수정 성공(200_OK)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            updated_article = Article.objects.create(
                user=self.user, 
                title=self.new_articles[i]["title"], 
                content=self.new_articles[i]["content"]
                )
            
            serializer = ArticleSerializer(updated_article).data
            
            # 게시글 수정 됐는지
            self.assertEqual(response.data[1]["title"], serializer["title"])
            self.assertEqual(response.data[1]["content"], serializer["content"])


# view = ArticleDetailView, url name = "article_detail_view", method = delete
class ArticleDeleteTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test1@test.com", "password": "password"}
        cls.user = User.objects.create_user("test1@test.com", "password")
        
        cls.another_user_data = {"email": "else1@test.com", "password": "password"}
        cls.another_user = User.objects.create(email="else1@test.com", password="password", nickname="someone")
        cls.another_user.set_password("password")
        cls.another_user.save()
        
        cls.faker = Faker()
        cls.articles=[]
        for i in range(10):
            cls.articles.append(Article.objects.create(
                title=cls.faker.sentence(), 
                content=cls.faker.text(), 
                user=cls.user
                ))
        
        Article.objects.filter(id=5).delete()

    def setUp(self):
        self.user_token = self.client.post(reverse("token_obtain_pair"), self.user_data).data["access"]
        self.another_user_token = self.client.post(reverse("token_obtain_pair"), self.another_user_data).data["access"]


    # 게시글 삭제 성공(204_NO_CONTENT)
    def test_pass_delete_article(self):
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": 1}),
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 204)
        
        
    # 로그인 안하고 게시글 삭제 실패(401_UNAUTHORIZED)
    def test_fail_delete_article_if_not_logged_in(self):
        url = reverse("article_detail_view", kwargs={"article_id": 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 401)


    # 다른 사람의 게시글 삭제 실패(403_FORBIDDEN)
    def test_fail_delete_article_if_not_author(self):
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": 3}),
            HTTP_AUTHORIZATION = f"Bearer {self.another_user_token}"
        )
        self.assertEqual(response.status_code, 403)


    # 없는 게시글 삭제 실패(404_NOT_FOUND)
    def test_fail_delete_article_if_not_exist(self):
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": 5}),
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 404)
        

# view = LikeView, url name = "like_view", method = post
class LikeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.article_data = {"title": "test Title", "content": "test content"}
        cls.user = User.objects.create(
            email=cls.user_data["email"], 
            password=cls.user_data["password"], 
            nickname="test"
            )
        cls.user.set_password(cls.user_data["password"])
        cls.user.save()
        cls.article = Article.objects.create(**cls.article_data, user=cls.user)
        
        cls.faker = Faker()
        cls.viewers_data = []
        cls.viewers = []
        for i in range(10):
            cls.viewer_data = {
                "email": f"{cls.faker.unique.email()}",
                "password": f"{cls.faker.word()}"
            }
            cls.viewers_data.append(cls.viewer_data)
            cls.viewer = User.objects.create(**cls.viewer_data, nickname=cls.faker.unique.name())
            cls.viewer.set_password(cls.viewer_data["password"])
            cls.viewer.save()
            cls.viewers.append(cls.viewer)                    

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]
        self.viewer_tokens = []
        for i in range(10):
            self.viewer_tokens.append(self.client.post(
            reverse("token_obtain_pair"), self.viewers_data[i]
            ).data["access"])

    
    def test_pass_like_article(self):
        
        # 좋아요
        for i in range(10):
            response = self.client.post(
                path=reverse("like_view", kwargs={"article_id": 1}),
                HTTP_AUTHORIZATION=f"Bearer {self.viewer_tokens[i]}",
            )
            serializer = ArticleDetailSerializer(self.article).data
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'message': "좋아요"})
            self.assertEqual(serializer["like_count"], i+1)
        
        # 좋아요 취소
        for i in range(10):
            response = self.client.post(
                path=reverse("like_view", kwargs={"article_id": 1}),
                HTTP_AUTHORIZATION=f"Bearer {self.viewer_tokens[i]}",
            )
            serializer = ArticleDetailSerializer(self.article).data
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, {'message': "좋아요 취소"})
            self.assertEqual(serializer["like_count"], 9-i)


# view = CommentView, url name = "comment_view", method = post
class CommentCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.user = User.objects.create(
            email=cls.user_data["email"], 
            password=cls.user_data["password"], 
            nickname="test"
            )
        cls.user.set_password(cls.user_data["password"])
        cls.user.save()
        
        cls.article_data = {"title": "test Title", "content": "test content"}
        cls.comment_data = {"content": "test comment content"}
        
        cls.article = Article.objects.create(**cls.article_data, user=cls.user)

    def setUp(self):
        self.access_token = self.client.post(
            reverse("token_obtain_pair"), self.user_data
        ).data["access"]

    # 댓글 작성
    def test_pass_create_comment(self):
        response = self.client.post(
            path=reverse("comment_view", kwargs={"article_id": 1}),
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, "test comment content")


# view = CommentView, url name = "comment_view", method = get
class CommentReadTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article_author_data = {"email": "test@test.com", "password": "Test1234!"}
        cls.article_author = User.objects.create(
            email=cls.article_author_data["email"], 
            password=cls.article_author_data["password"], 
            nickname="test"
            )
        cls.article_author.set_password(cls.article_author_data["password"])
        cls.article_author.save()
        
        cls.article_data = {"title": "test Title", "content": "test content"}
        cls.article = Article.objects.create(**cls.article_data, user=cls.article_author)
        
        cls.faker = Faker()
        cls.comments=[]
        for i in range(10):
            cls.user = User.objects.create(
                email=cls.faker.unique.email(), 
                password=cls.faker.word(), 
                nickname=cls.faker.unique.name()
                )
            cls.comments.append(Comment.objects.create(
                content=cls.faker.text(),
                article=cls.article,
                user=cls.user
                ))


    # 특정 게시글의 댓글 리스트 모두 보기(10개) 성공
    def test_pass_comment_list(self):
        
        response = self.client.get(path=reverse("comment_view", kwargs={"article_id": 1}))
        
        # 댓글 조회 요청(200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 댓글 정보 최신순으로
        for i in range(10):
            self.assertEqual(response.data[i]["content"], self.comments[-(i+1)].content)
            self.assertEqual(response.data[i]["user"]["nickname"], self.comments[-(i+1)].user.nickname)
            
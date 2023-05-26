from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
# 이미지
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

from faker import Faker

from users.models import User
from articles.models import Article
from articles.serializers import ArticleDetailSerializer


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


    # 다른 사람의 게시글 삭제 실패(401_UNAUTHORIZED)
    def test_fail_delete_article_if_not_author(self):
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": 3}),
            HTTP_AUTHORIZATION = f"Bearer {self.another_user_token}"
        )
        self.assertEqual(response.status_code, 403)


    # 없는 게시글 삭제 실패(404_NOT_FOUND)
    def test_fail_delete_article_if_not_exist(self):
        response = self.client.delete(
            path = reverse("article_detail_view", kwargs={"article_id": 11}),
            HTTP_AUTHORIZATION = f"Bearer {self.user_token}"
        )
        self.assertEqual(response.status_code, 404)
        
# Yoriking

## 프로젝트 설명
요리킹조리킹은 음식관련 커뮤니티로, 좋아하는 음식에 관한 이야기를 나눌 수 있는 커뮤니티입니다.

## 주요 기능
- 회원 기능
  - 카카오 소셜 로그인
  - JWT 토큰 기반 인증
  - 유저 프로필 조회
  - 유저 팔로우 기능

- 게시글 기능
  - 카테고리 별 게시글 작성
  - 댓글
  - 좋아요

- 조리킹 AI
  - YOLOv8 기반으로 학습된 인공지능으로, 냉장고나 식재료 사진을 업로드 하면 AI가 재료를 인식해 해당 재료들로 만들 수 있는 요리를 추천해드립니다.

## 개발 환경
- Python 3.11.3
- Django 4.2.1
- Django-Rest-Framework==3.14.0
- YOLOv8

## ERD 설계
![image](https://github.com/choice44/yoriking/assets/126167661/eaa6ecc3-5675-4be6-bde2-78268d93d117)

## API 설계

[카카오 로그인](https://www.notion.so/222a10d362b5484288d158f0d283a870)

[토큰 로그인](https://www.notion.so/6cb53347a73049579485f473db652f59)

[토큰 리프레시](https://www.notion.so/b0076c2858de44b1b24366506463915d)

[마이페이지 요청](https://www.notion.so/0654f500456846aea82039fe28416e43)

[타인페이지 요청](https://www.notion.so/d7d9543a916a471e87f0d4f0c3462d57)

[회원 프로필 수정](https://www.notion.so/3f7eff48d3e24f13a83b64eced99bca0)

[회원 탈퇴 요청](https://www.notion.so/564748f8efa94e1cb81537e332d6abb4)

[팔로우 요청/취소](https://www.notion.so/253a838dc52145658d0d17ab235275a7)

[전체 게시글 조회](https://www.notion.so/61a295c035694d178e50acb849f03128)

[게시글 작성](https://www.notion.so/cdb52058f3474e6c8df975c57b9e13d8)

[게시글 상세](https://www.notion.so/e1b79d47e0af4ed391a043ba1bed7822)

[게시글 수정](https://www.notion.so/e5dd6b6cdfbc4ccdb0d2821a8282e25a)

[게시글 삭제](https://www.notion.so/e5c791f78d064d9296c9146043ebdd4f)

[댓글 조회](https://www.notion.so/663659743cc044f4875dc10c9d8d8553)

[댓글 작성](https://www.notion.so/082672a9440447918e61ce7ed2633d39)

[댓글 수정](https://www.notion.so/ce221c5f498a47298f4a125caa7d1c65)

[댓글 삭제](https://www.notion.so/be0c2a0ffb534f54995c64141786fc8e)

[좋아요 요청/취소](https://www.notion.so/65d78f26a42540d7a90c026be4cf3e8a)

[냉장고 사진 재료 파악해서 요리 추천](https://www.notion.so/ffdf8d72e2de473fa95711946ae65c63)

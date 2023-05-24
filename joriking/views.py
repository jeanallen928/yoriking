from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import JorikingSerializer
from .models import Joriking

from ultralytics import YOLO
import cv2
import openai
import os

openai.api_key = os.environ.get("openai_api_key")

class JorikingView(APIView):
    def post(self, request):
        serializer = JorikingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # YOLOv8 로 학습한 모델로 이미지 상의 식재료를 추출
        model = YOLO("jorikingV3.pt")
        names = model.names
        img = cv2.imread(serializer.data['image'][1:])
        ingredients = []
        
        results = model.predict(source=img, stream=True)
        for result in results:
            for cls in result.boxes.cls:
                ingredients.append(names[int(cls)])
        
        ingredient_set = set(ingredients) # 중복 제거
        igds = ', '.join(ingredient_set)
        
        # ChatGPT
        gpt_prompt = []

        gpt_prompt.append({
            "role": "system",
            "content": "Ingredients will be given, suggest some dishes and recipes that can be based on the given ingredients. answer in korean"
        })

        gpt_prompt.append({
            "role": "user",
            "content": igds
        })

        prompt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt)
        prompt = prompt["choices"][0]["message"]["content"]
        
        # 데이터와 이미지 파일 삭제
        os.remove(serializer.data['image'][1:])
        data = Joriking.objects.get(id=serializer.data["id"])
        data.delete()
        
        return Response({"result": prompt})

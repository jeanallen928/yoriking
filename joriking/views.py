from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import JorikingSerializer

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
        
        model = YOLO("jorikingV2.pt")
        names = model.names
        img = cv2.imread(serializer.data['image'][1:])
        ingredients = []
        
        results = model.predict(source=img, stream=True)
        for result in results:
            for cls in result.boxes.cls:
                ingredients.append(names[int(cls)])
        
        igds = ', '.join(ingredients)
        print(igds)
        
        # ChatGPT
        gpt_prompt = []

        gpt_prompt.append({
            "role": "system",
            "content": "Ingredients will be given, so please recommend some dishes and recipes that can be based on the given ingredients. in korean"
        })

        gpt_prompt.append({
            "role": "user",
            "content": igds
        })

        
        prompt = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt)
        prompt = prompt["choices"][0]["message"]["content"]
        print(prompt)
        return Response({"message": "POST 요청"})

from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import JorikingSerializer


class JorikingView(APIView):
    def post(self, request):
        serializer = JorikingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "POST 요청"})

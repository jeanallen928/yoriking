from rest_framework import serializers
from .models import Joriking


class JorikingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joriking
        fields = ["image",]
        
        
        
        
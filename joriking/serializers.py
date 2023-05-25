from rest_framework import serializers
from .models import Joriking


class JorikingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joriking
        fields = "__all__"
        extra_kwargs = {
            "pred_path": {
                "read_only": True
            },
            "ingredients": {
                "read_only": True
            },
        }
      
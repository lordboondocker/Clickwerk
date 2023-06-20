from rest_framework.serializers import ModelSerializer
from .models import Core


class CoreSerializers(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power']

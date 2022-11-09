from rest_framework import serializers
from .models import appEmailDataModel


class appFromEmailSearchSerializer(serializers.Serializer):
    email = serializers.EmailField()



class appEmailDataModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = appEmailDataModel
        fields = "__all__"

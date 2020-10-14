from rest_framework import serializers
from questionbox import models


class QuestionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, max_length=255)
    body = serializers.CharField(required=True, allow_blank=False)

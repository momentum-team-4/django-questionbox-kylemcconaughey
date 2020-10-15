from rest_framework import serializers
from questionbox.models import Question


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=255)
    body = serializers.CharField(required=True, allow_blank=False)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(required=True, allow_blank=False)
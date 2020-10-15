from rest_framework import serializers
from questionbox.models import Question, Answer
from users.models import User


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "title", "body", "user"]

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class AnswerSerializer(serializers.Serializer):
    class Meta:
        model = Answer
        fields = ["id", "body"]


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "questions"]

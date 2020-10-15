from rest_framework import serializers
from questionbox.models import Question, Answer
from users.models import User


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Question
        fields = ["url", "id", "title", "body", "user"]

    def create(self, validated_data):
        return Question.objects.create(**validated_data)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "body"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(
        many=True, view_name="question-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "questions"]

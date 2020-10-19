from rest_framework import serializers
from questionbox.models import Question, Answer
from users.models import User


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["url", "body", "question"]


class EmbeddedAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "url", "body"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(
        many=True, view_name="question-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "questions"]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    answers = EmbeddedAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "title",
            "id",
            "url",
            "user",
            "body",
            "answers",
        ]

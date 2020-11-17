from rest_framework import serializers
from questionbox.models import Question, Answer
from users.models import User


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["author", "id", "url", "body", "isCorrect", "question"]


class EmbeddedAnswerSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "author", "url", "isCorrect", "body"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(
        many=True, view_name="question-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["username", "id", "url", "questions"]


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

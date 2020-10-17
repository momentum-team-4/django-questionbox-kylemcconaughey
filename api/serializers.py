from rest_framework import serializers
from questionbox.models import Question, Answer


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ["url", "body", "question"]


class EmbeddedAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = [
            "url",
            "body",
        ]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    answers = EmbeddedAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["url", "title", "body", "answers", "user"]

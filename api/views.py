from django.core.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from questionbox.models import Question, Answer
from .serializers import AnswerSerializer, QuestionSerializer

"""
GET    /api/questions/      Get a list of all questions you are allowed to see
POST   /api/questions/      Create a new question
GET    /api/questions/<id>/ Get one question
PUT    /api/questions/<id>/ Replace a question
PATCH  /api/questions/<id>/ Update a question
DELETE /api/questions/<id>/ Delete a question
POST   /api/answers/       Add an answer to a question
PATCH  /api/answers/<pk>/  Update an answer
PATCH  /api/answers/<pk>/  Delete an answer
"""


class WroteOrRead(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user == request.user:
            return True

        return False


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    permission_classes = [
        WroteOrRead,
    ]

    def get_queryset(self):
        return Question.objects.all()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)
        raise PermissionDenied()


class AnswerCreateView(CreateAPIView):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied()
        serializer.save(author=self.request.user)


class AnswerDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AnswerSerializer

    def get_queryset(self):
        if not self.request.user == Answer.author:
            raise PermissionDenied()
        return Answer.objects.filter(author=self.request.user)

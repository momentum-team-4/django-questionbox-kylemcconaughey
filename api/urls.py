from django.urls import include, path
from rest_framework import routers

from . import views as api_views

api_router = routers.DefaultRouter()
api_router.register("questions", api_views.QuestionViewSet, basename="question")
api_router.register("answers", api_views.AnswerViewSet, basename="answer")
api_router.register("users", api_views.UserViewSet, basename="user")

urlpatterns = [
    path("", include(api_router.urls)),
]
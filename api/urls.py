from django.urls import include, path
from rest_framework import routers

from . import views as api_views

api_router = routers.DefaultRouter()
api_router.register("questions", api_views.QuestionViewSet, basename="question")

urlpatterns = [
    path("answers/", api_views.AnswerCreateView.as_view(), name="answer-list"),
    path(
        "answers/<int:pk>/",
        api_views.AnswerDetailView.as_view(),
        name="answer-detail",
    ),
    path("", include(api_router.urls)),
]
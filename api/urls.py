from django.urls import include, path
from rest_framework import routers

from api import views as api_views

api_router = routers.DefaultRouter()
api_router.register("recipes", api_views.RecipeViewSet, basename="recipe")

urlpatterns = [
    path(
        "answers/", api_views.AnswerCreateView.as_view(), name="answer-list"
    ),
    path(
        "answers/<int:pk>/",
        api_views.AnswerDetailView.as_view(),
        name="answer-detail",
    ),
    path("", include(api_router.urls)),
]
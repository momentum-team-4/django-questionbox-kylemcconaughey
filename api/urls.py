from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

# API endpoints
urlpatterns = format_suffix_patterns(
    [
        path("", views.api_root),
        path("api_questions/", views.QuestionList.as_view(), name="question-list"),
        path(
            "api_questions/<int:pk>/",
            views.QuestionDetail.as_view(),
            name="question-detail",
        ),
        path("api_users/", views.UserList.as_view(), name="user-list"),
        path("api_users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    ]
)
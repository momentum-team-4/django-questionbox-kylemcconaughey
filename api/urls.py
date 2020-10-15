from django.urls import path
from . import views as api_views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path("api/", api_views.question_list),
    path("api/<int:pk>/", api_views.question_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)

"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from questionbox import views as questionbox_views
from users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("registration.backends.simple.urls")),
    path("", questionbox_views.frontpage, name="frontpage"),
    path(
        "question/<int:pk>/", questionbox_views.question_detail, name="question_detail"
    ),
    path("question/create/", questionbox_views.question_create, name="question_create"),
    path(
        "question/delete/<int:pk>",
        questionbox_views.question_delete,
        name="question_delete",
    ),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

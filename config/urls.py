# config/urls.py
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path

from api.schema import api as ninja_api

urlpatterns = [
    # Root → redirect to API docs
    path("", lambda request: HttpResponseRedirect("/api/docs/")),
    # Admin
    path("admin/", admin.site.urls),
    # API (Django Ninja)
    path("api/", ninja_api.urls),
]

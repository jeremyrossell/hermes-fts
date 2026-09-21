from django.urls import path
from .views import search_api

urlpatterns = [
    path('search/', search_api, name='search_api'),
]
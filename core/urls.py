from django.urls import path
from core import views

urlpatterns = [
    path('api/sentiment/', views.sentiment_analysis, name='sentiment_analysis'),
]

"""
Chat app URL configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('message/', views.send_message, name='chat_message'),
    path('feedback/', views.submit_feedback, name='chat_feedback'),
    path('suggestions/', views.get_suggestions, name='chat_suggestions'),
]

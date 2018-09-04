from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('Chatbot_iframe', views.Chatbot_iframe, name='Chatbot_iframe'),
    path('Chatbot_sub', views.Chatbot_sub, name='Chatbot_sub'),
]
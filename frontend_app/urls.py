from django.urls import path
from chat_app.views import ContentView,GetMessagesView
from .views import index


app_name = 'frontend_app'

urlpatterns = [
    path("test/", ContentView.as_view()),
    path("", index),
    path("chat/", index),
    path("test3/", GetMessagesView.as_view()),
]
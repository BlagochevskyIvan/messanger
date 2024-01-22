from django.urls import path, include
from chat_app.views import main, chat, video, search_user, create_dialog, get_messages, send_message, DialogsView, ContentView, GetMessagesView
from frontend_app.views import index


app_name = "chat_app"

urlpatterns = [
    # path("", main, name="main"),
    path("chat/", chat, name="chat"),
    path("video/", video, name="video"),
    path("chat/search_user", search_user, name="search_user"),
    path("chat/create_dialog/<int:id_user>", create_dialog, name="create_dialog"),
    path("chat/get_messages", get_messages, name="get_messages"),
    path("chat/sendmessage", send_message, name="send_message"),
]

from django.urls import path, include
from chat_app.views import chat, conf, search_user, create_dialog, get_messages, send_message,get_messages_list

app_name = "chat_app"

urlpatterns = [
    path("", chat, name="chat"),
    path("chat/search_user", search_user, name="search_user"),
    path("chat/create_dialog/<int:id_user>", create_dialog, name="create_dialog"),
    path("chat/get_messages_list/<dialog_id>", get_messages_list, name="get_messages_list"),
    path("chat/get_messages", get_messages, name="get_messages"),
    path("chat/sendmessage", send_message, name="send_message"),
    path("conf/", conf, name="conf"),
]

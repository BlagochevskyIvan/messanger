"""
URL configuration for siteproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

# from frontend.views import index

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("user/", include("user_app.urls", "user_app")),
#     path("", mainplug, name="main"),
#     path("sign_in/", main),
#     path("settings/", usersettings),
#     path("conf/", conf),
#     path("checkform", checkform),
#     path("favicon.ico/", favicon),
#     path("send_message/", send_message),
#     path("get_messages/<str:room_id>/", get_messages),
#     path("<str:roomname>/", dialog),
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("user_app.urls", "user_app")),
    path("chat/", include("chat_app.urls", "chat_app")),
    path("", include("frontend_app.urls", "frontend_app")),
    #path("tich/", index),
    # path("conf/", conf)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



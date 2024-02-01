from django.urls import path, include
from user_app.views import reg, usersettings, sign_in, logout


app_name = "user_app"

urlpatterns = [
    path("", sign_in, name='main'),
    path('sign_up/', reg, name='sign_up'),
    path("settings/", usersettings, name ='settings'),
    path("logout/",logout ,name="logout")
]
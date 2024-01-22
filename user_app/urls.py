from django.urls import path, include
from user_app.views import login, reg, usersettings, main, sign_in, logout


app_name = "user_app"

urlpatterns = [
    path("", main, name='main'),
    path('sign_up/', reg, name='reg'),
    path("sign_in/", sign_in, name='sign_in'),
    path("settings/", usersettings, name ='settings'),
    path("logout/",logout ,name="logout")
]
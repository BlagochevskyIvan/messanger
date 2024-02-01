from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from user_app.forms import UserLoginForm, UserRegForm
from django.contrib import auth

def sign_in(request):
    if request.method == 'GET':
        # if request.user.is_authenticated:
        #     return HttpResponseRedirect(reverse('chat_app:main'))
        user_form = UserLoginForm()
    else:
        print(request.POST)
        user_form = UserLoginForm(data = request.POST)
        if user_form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            print(user)
            if user:
                auth.login(request, user)
                # Успешный вход
                return HttpResponseRedirect(reverse('chat_app:chat'))
    context = {
            "form": user_form,
        }
    return render(request, "user_app/sign_in.html", context)

def login(request):
    return HttpResponse("Ответ")


def reg(request):
    if request.method == "GET":
        user_reg = UserRegForm()
    else:
        user_reg = UserRegForm(data = request.POST)
        print(user_reg.errors)
        if user_reg.is_valid():
            print('valid')
            user_reg.save()
            return HttpResponseRedirect(reverse('user_app:sign_in'))
    context = {
        "registration": user_reg
    }
    return render(request, 'user_app/registration.html', context)

def usersettings(request):
    return HttpResponse("настройки")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user_app:main'))

def settings(request):
    return render()
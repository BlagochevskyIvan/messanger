from django.shortcuts import render, HttpResponse

def mainplug(request):
    return HttpResponse("главная")

def conf(request):
    return HttpResponse("Конференции")

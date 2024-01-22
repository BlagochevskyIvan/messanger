from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from chat_app.models import *
from user_app.models import User
from django.http import JsonResponse
from rest_framework import generics

from .serializers import *


# Create your views here.

def main(request):
    # print(Dialog.objects.all()[0])
    # print(Dialog.objects.all()[0].name)
    print(User.objects.filter(is_superuser = 1 ))
    print(User.objects.filter(first_name = 'Ибрагим'))
    print(User.objects.get(username = '123'))

    user = User.objects.get(id=4)
    print(user.first_name, user.last_name)
    user.first_name = 'Floppa'
    print(user.first_name, user.last_name)
    user.save()
    print(request.user) # Твой нынешний аккаунт
    print(Message.objects.first().author)
    # mes1 = Message.objects.create(text='Че ваще?', author=user, type_message_id=1)
    # mes2 = Message.objects.create(text='Че ваще?2', author_id=4, type_message_id=1)
    # mes1.save()
    # mes2.save()
    return render(request, 'chat_app/main.html')

def chat(request):
    dialog_requested_id = request.GET.get('dialog')
    # print(Member.objects.filter(user = request.user))
    dialogs_by_user = Member.objects.filter(user = request.user)
    context = {'dialogs': [], 'messages': None}
    for dialog in dialogs_by_user:
        dialog_info = Dialog.objects.get(id = dialog.dialog_id)
        print(dialog_info.avatar)
  
        if dialog_info.category_id == 1:
            dialogs_by_id = Member.objects.filter(dialog_id = dialog.dialog_id).exclude(user = request.user)
            if not dialogs_by_id.exists():
                dialog_name = "Избранное"
            else:
                dialog_name = dialogs_by_id[0].user.username
        else:
            dialog_name = dialog_info.name
        context['dialogs'].append({'dialog_info':dialog_info, 'name':dialog_name})
    if dialog_requested_id != None:
        messages = get_messages(request, int(dialog_requested_id))
        context['messages'] = messages
        context['current_dialog'] = int(dialog_requested_id)

    return render(request, 'chat_app/chat.html', context)

def search_user(request):
    users = User.objects.filter(username__contains = request.GET.get('username'))
    search = {'users': users}
    return render(request, 'chat_app/searched.html', search)

def video(request):
    return render(request, 'chat_app/video.html')

def create_dialog(request, id_user):
    dialogs = Member.objects.filter(user_id__in = [id_user, request.user.id]).order_by('dialog_id')
    current_id = 0
    count = 0
    if id_user != request.user.id:
        for dialog in dialogs:
            if dialog.dialog_id == current_id:
                count += 1
            else:
                count = 1
                current_id = dialog.dialog_id
            if count == 2:
                if dialog.dialog.category_id == 1:
                    # Переводим человека в этот диалог
                    print(dialog)
                    return HttpResponseRedirect(f'/chat/chat/?dialog={dialog.dialog.id}')
                    break
        else:
            # создаем диалог
            dia = Dialog.objects.create(category_id = 1, name = '')
            dia.save()
            if id_user != request.user.id:
                member1 = Member.objects.create(dialog = dia, user_id = id_user)
                member1.save()
            member2 = Member.objects.create(dialog = dia, user_id = request.user.id)
            member2.save()
            return HttpResponseRedirect(f'/chat/chat/?dialog={dia.id}')

def dialog(request):
    return render(request, 'chat_app/dialog.html')


def get_messages(request, dialog_id):
    content = Content.objects.filter(dialog_id=dialog_id)
    return content
    # return JsonResponse({"messages": list(messages.values())})

def send_message(request):
    user_id = request.POST['user_id']
    dialog_id = request.POST['dialog_id']
    text = request.POST['text']
    message = Message.objects.create(text = text, author_id = user_id, type_message_id = 1)
    message.save()
    content = Content.objects.create(dialog_id = dialog_id, message_id = message.id)
    content.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DialogsView(generics.ListAPIView):
    queryset = Dialog.objects.all()
    serializer_class = DialogSerializer

class ContentView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

class GetMessagesView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        dialog_id = 1
        content = Content.objects.filter(dialog_id = dialog_id).values_list('message_id', flat = True)
        messages = Message.objects.filter(id__in = content)
        return messages

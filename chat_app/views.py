from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from chat_app.models import *
from user_app.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

@login_required
def chat(request):
    dialog_requested_id = request.GET.get('dialog')
    # print(Member.objects.filter(user = request.user))
    dialogs_by_user = Member.objects.filter(user = request.user)
    context = {'dialogs': [], 'messages': None, 'user_id': request.user.id}
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

def conf(request):
    return render(request, 'chat_app/conf.html')

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
                    return HttpResponseRedirect(f'/?dialog={dialog.dialog.id}')
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
            return HttpResponseRedirect(f'/?dialog={dia.id}')

def dialog(request):
    return render(request, 'chat_app/dialog.html')


def get_messages(request, dialog_id):
    content = Content.objects.filter(dialog_id=dialog_id)
    return content
    # return JsonResponse({"messages": list(messages.values())})

def get_messages_list(request, dialog_id):
    content = Content.objects.filter(dialog_id=dialog_id).values_list('message_id', flat=True)
    messages = list(Message.objects.filter(id__in=content).values())
    return JsonResponse({'messages': messages})

def send_message(request):
    user_id = request.POST['user_id']
    dialog_id = request.POST['dialog_id']
    text = request.POST['text']
    message = Message.objects.create(text = text, author_id = user_id, type_message_id = 1)
    message.save()
    content = Content.objects.create(dialog_id = dialog_id, message_id = message.id)
    content.save()
    return HttpResponse('Отправлено')




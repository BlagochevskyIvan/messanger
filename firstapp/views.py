from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from firstapp.models import Message, Room
from user_app.forms import UserLoginForm
from django.contrib import auth


# Create your views here.
def main(request):
    if request.method == 'GET':
        # print(request.session.keys())
        # print(request.GET.get("username"))
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
    context = {
            "form": user_form,
        }
    return render(request, "firstapp/rooms.html", context)



def checkform(request):
    username = request.POST["username"]
    roomname = request.POST["roomname"]
    print(f"Я запустил функцию checkform login {username} room {roomname}")
    room = Room.objects.filter(name=roomname)
    if room.exists():
        print("Я перенаправляю")
        return redirect(f"/{roomname}/?username={username}")
    else:
        new_room = Room.objects.create(name=roomname)
        new_room.save()
        print("Я создаю комнату")
        return redirect(f"/{roomname}/?username={username}")


def dialog(request, roomname):
    username = request.GET.get("username")

    room_details = Room.objects.all()
    print(
        f"Я запустил функцию диалог login {username} room {roomname} {room_details.filter(name=roomname)}"
    )

    room_info = Room.objects.get(name=roomname)
    context = {
        "roomname": roomname,
        "room_info": room_info,
        "username": username,
    }

    return render(request, "firstapp/dia.html", context)


def send_message(request):
    print("Функция send_message")
    username = request.POST["username"]
    room_id = request.POST["room_id"]
    message = request.POST["message"]
    new_message = Message.objects.create(user=username, room=room_id, text=message)
    new_message.save()

    return HttpResponse("Успешно отправлено")


def favicon(request):
    return HttpResponse("")


def get_messages(request, room_id):
    messages = Message.objects.filter(room=int(room_id))
    return JsonResponse({"messages": list(messages.values())})

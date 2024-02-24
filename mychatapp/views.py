from django.shortcuts import render, redirect
from mychatapp.models import Profile, Friend, ChatMessage
from mychatapp.forms import ChatMessageForm
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required
def index(request):
    user = request.user.profile
    friends = user.friends.all()
    context = {"user": user, "friends": friends}
    return render(request, "mychatapp/index.html", context)

@login_required
def detail(request, pk):
    friend = Friend.objects.get(profiles_id=pk)
    user = request.user.profile
    profile = Profile.objects.get(id=friend.profiles.id)
    chats =ChatMessage.objects.all()
    res_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
    res_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profiles.id)
    context = {
        "friend": friend,
        "form": form,
        "user": user,
        "profile": profile,
        "chats": chats,
        "num": res_chats.count(),
    }
    return render(request, "mychatapp/detail.html", context)

@login_required
def sentMessages(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profiles_id=pk)
    profile = Profile.objects.get(id=friend.profiles.id)
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False)
    return JsonResponse(new_chat_message.body, safe=False)

@login_required
def receiveMessage(request, pk):
    user = request.user.profile
    friend = Friend.objects.get(profiles_id=pk)
    profile = Profile.objects.get(id=friend.profiles.id)
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)


def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    arr = []
    for friend in friends:
        chats = ChatMessage.objects.filter(msg_sender__id=friend.profiles.id, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)
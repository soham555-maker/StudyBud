from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

# rooms = [
#     {"id":1, "name":"Let's learn python!"},
#     {"id":2, "name":"Mastering DSA"},
#     {"id":3, "name":"Discovering Back-End with django"},
# ]

# Create your views here.

@login_required(login_url='login-page')
def createRoom(request):
    form = RoomForm()
    context = {'form' : form}
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            room.participants.add(request.user)
        return redirect('home')
    return render(request, 'base/room_form.html', context)

def loginPage(request):
    page = 'login'
    context = {'page' : page}
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'The user does not exist.')
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'The username or password does not exist.')  

    return render(request, 'base/login_register.html', context)

@login_required(login_url='login-page')
def logoutPage(request):
    context = {}
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form' : form}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'oops, something went wrong, Please try again.')  

    return render(request, 'base/login_register.html', context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )
    room_messages = Message.objects.filter(
        Q(Room__topic__name__icontains = q) |
        Q(Room__name__icontains = q)
        # Q(room__topic__icontains = q)
    )
    rooms_count = rooms.count()
    topics = Topic.objects.all()
    context = {
        'rooms': rooms,
        'topics': topics,
        'rooms_count': rooms_count,
        'room_messages': room_messages,
        }
    return render(request, 'base/home.html',context)

def profilePage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {
        'user': user,
        'rooms': rooms,
        'room_messages':room_messages,
        'topics': topics,
    }
    return render(request, 'base/profile.html', context )

def about(request):
    return render(request, 'base/about.html')

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method =='POST':
        message = Message.objects.create(
            user=request.user,
            Room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room' : room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)

@login_required(login_url='login-page')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!!!!!")

    context = {'form' : form}
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
        return redirect('home')
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login-page')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !!!!!!")

    context = {'obj' : room}
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)

@login_required(login_url='login-page')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here !!!!!!")

    context = {'obj' : message}
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context)





from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .forms import UserForm
from .serializers import UserSerializer, UserSerializerDetail


# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail


def index(request):
    user = User.objects.filter(id=request.user.id)
    if len(user) != 0:
        return render(request, 'index.html')
    else:
        return redirect('login')


class Login(APIView):
    def get(self, request):
        return render(request, 'login.html', {'invalid': False})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'invalid': True})


def user_logout(request):
    logout(request)
    return redirect('login')


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'registration.html', {'invalid': False, 'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            existing_user = User.objects.filter(username=username)
            if len(existing_user) == 0:
                password = form.cleaned_data['password']
                user = User.objects.create_user(username, '', password)
                user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                return redirect('index')
            else:
                return render(request, 'registration.html', {'invalid': True, 'form': form})

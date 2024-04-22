from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    return render(request, 'main/user_page.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main:user_page'))
        else:
            form = AuthenticationForm()
            return render(request, 'users/login.html', {
                'message': 'Incorrect Username or Password',
                "form": form
            })
    form = AuthenticationForm()
    return render(request, 'users/login.html', {"form": form})


def logout_view(request):
    logout(request)
    form = AuthenticationForm()
    return render(request, 'users/login.html', {
        'message': 'Logged Out!',
        "form": form
    })


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            login_form = AuthenticationForm()
            return render(response, 'users/login.html', {
                'message': 'You are now registered!',
                'form': login_form
            })
    else:
        form = RegisterForm()
        return render(response, "users/register.html", {"form": form})

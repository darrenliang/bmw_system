from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status, authentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


def login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect(reverse('rooms'))
            return redirect(reverse('log_in'))
        # else:
        #     logger.info("[log_in] errors={}".format(form.errors))

    return render(request, 'bmw/login.html', {'form': form})


def overview(request):
    return render(request, 'bmw/overview.html')


def devices(request):
    return render(request, 'bmw/devices.html')


def charts(request):
    return render(request, 'bmw/charts.html')


def details(request):
    return render(request, 'bmw/details.html')


def setting(request):
    return render(request, 'bmw/settings.html')


def audit_logs(request):
    return render(request, 'bmw/audit_logs.html')


def web_socket(request):
    return render(request, 'bmw/web_socket.html')


@login_required(login_url='/login/')
def logout(request):
    logout(request)
    return redirect(reverse('login'))


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('log_in'))
        # else:
        #     logger.info("[sign_up] errors={}".format(form.errors))
    return render(request, 'bmw/sign_up.html', {'form': form})



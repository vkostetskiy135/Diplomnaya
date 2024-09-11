import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .forms import UserForm, EditProfileForm
from .models import User


def main_page(request):
    return render(request, 'main_page.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username, password=password)
            return redirect(f'/profile/{user.slug}')
        except User.DoesNotExist:
            print(f"User {username} does not exist")
            return HttpResponse("User not found", status=404)


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html',
                          {"error": "Пользователь с таким логином уже существует."})

        user = User.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age,
            slug=username.lower()
        )

        return redirect(f'/profile/{user.slug}')

    return render(request, 'register.html')


def profile(request, slug):
    try:
        user = User.objects.get(slug=slug)
        return render(request, 'profile.html', {"user": user})
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)


def edit_profile(request, slug):
    try:
        user = User.objects.get(slug=slug)
        return render(request, 'edit_profile.html', {"user": user})
    except User.DoesNotExist:
        return redirect(f'/profile/{slug}')


def update_profile(request, slug):
    if request.method == 'POST':
        try:
            user = User.objects.get(slug=slug)
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.age = request.POST.get('age')
            user.save()
            return redirect(f'/profile/{user.slug}')
        except User.DoesNotExist:
            return redirect(f'/profile/{slug}')
    return redirect(f'/edit_profile/{slug}')


def upload_avatar(request, slug):
    if request.method == "POST" and request.FILES.get('avatar'):
        user = User.objects.get(slug=slug)
        user.avatar = request.FILES['avatar']
        user.save()
        return redirect('profile', slug=user.slug)
    return render(request, 'profile.html')


def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, EditProfileForm, IdeaForm
from .models import User, Idea


def main_page(request):
    return render(request, 'main_page.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(f'/profile/{user.slug}')
        else:
            return HttpResponse("Invalid credentials", status=401)
    return render(request, 'main_page.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        age = request.POST.get("age")

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {"error": "Пользователь с таким логином уже существует."})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age
        )

        login(request, user)
        return redirect(f'/profile/{user.slug}')

    return render(request, 'register.html')


@login_required
def profile(request, slug):
    try:
        user = User.objects.get(slug=slug)
        return render(request, 'profile.html', {"user": user})
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)


@login_required
def edit_profile(request, slug):
    user = User.objects.get(slug=slug)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=user.slug)
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'edit_profile.html', {'form': form, 'user': user})


@login_required
def upload_avatar(request, slug):
    if request.method == "POST" and request.FILES.get('avatar'):
        try:
            user = User.objects.get(slug=slug)
            user.avatar = request.FILES['avatar']
            user.save()
            return redirect('profile', slug=user.slug)
        except User.DoesNotExist:
            return HttpResponse("User not found", status=404)
    return render(request, 'profile.html')


def user_logout(request):
    logout(request)
    return redirect('main_page')


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})


def project_page(request):
    return render(request, 'project_page.html')


@login_required
def add_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            return redirect('profile', slug=request.user.slug)
    else:
        form = IdeaForm()
    return render(request, 'add_idea.html', {'form': form})


@login_required
def edit_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=request.user.slug)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'edit_idea.html', {'form': form, 'idea': idea})


@login_required
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    idea.delete()
    return redirect('profile', slug=request.user.slug)



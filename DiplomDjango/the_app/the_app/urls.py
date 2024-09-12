"""
URL configuration for the_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from user import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('user/login/', views.user_login, name='user_login'),
    path('register/', views.register, name='register'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('edit_profile/<slug:slug>/', views.edit_profile, name='edit_profile'),
    path('upload_avatar/<slug:slug>/', views.upload_avatar, name='upload_avatar'),
    path('users/', views.user_list, name='user_list'),
    path('project_page/', views.project_page, name='project_page'),
    path('logout/', auth_views.LogoutView.as_view(next_page='main_page'), name='logout'),
    path('add_idea/', views.add_idea, name='add_idea'),
    path('edit_idea/<int:pk>/', views.edit_idea, name='edit_idea'),
    path('delete_idea/<int:pk>/', views.delete_idea, name='delete_idea'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
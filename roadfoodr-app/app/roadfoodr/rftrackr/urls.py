""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/v1/users/', views.api_users_get_json, name='Retrieve all users'),
    path('api/v1/users/<int:user_id>/', views.api_user_get_json, name='Retrieve one user'),
    path('api/v1/users/<int:user_id>/delete', views.api_user_delete, name='Delete user'),
    path('api/v1/users/<int:user_id>/update', views.api_user_update, name='Update user'),
    path('api/v1/users/create', views.api_user_create, name='Create user'),
]

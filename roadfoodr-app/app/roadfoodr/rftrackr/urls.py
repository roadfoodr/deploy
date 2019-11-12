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
from . import views, views_api, views_admin

urlpatterns = [
    path('', views.index, name='index'),
    path('testpage', views.testpage, name='testpage'),

    path('api/v1/users/', views_api.api_users_get_json, name='Retrieve all users'),
    path('api/v1/users/<int:user_id>/', views_api.api_user_get_json, name='Retrieve one user'),
    path('api/v1/users/<int:user_id>/delete', views_api.api_user_delete, name='Delete user'),
    path('api/v1/users/<int:user_id>/update', views_api.api_user_update, name='Update user'),
    path('api/v1/users/create', views_api.api_user_create, name='Create user'),
    path('recordUser', views_api.api_record_user, name='Record User'),
    
    path('admin/visualization', views_admin.admin_visualization, name='Visualize user logs'),
]

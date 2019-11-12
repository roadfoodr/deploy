from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings


def admin_visualization(request):
    return render(request, 'admin/visualization.html')

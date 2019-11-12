from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import os, json, logging

from rftrackr.models import User, Roadfood, Visit


def index(request):
    return render(request, 'index.html')
def testpage(request):
    return render(request, 'testpage.html')

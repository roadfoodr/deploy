from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
import os, json, logging
import requests
from collections import OrderedDict

from rftrackr.models import User, Roadfood, Visit


'''
Utility functions
'''

LOG_USER_VISITS_LOCALLY = False
LOG_USER_VISITS_URL = 'https://5vcfjcukc9.execute-api.us-east-2.amazonaws.com/default/analytics'

USER_REQUIRED_FIELDS = {'name_first', 'name_last'}
USER_AUTO_FIELDS = {'user_id'}

DEBUG_LOGGER = logging.getLogger(__name__)



def result_with_status(result=None, status=None):
    ''' utility function to add status message to result structure '''
    response = {}
    response['status'] = status
    response['result'] = result if result else {}
    return response

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', None)
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip

def log_user_visit(post_data=None):
    if post_data is None:
        return
    if LOG_USER_VISITS_LOCALLY:
        os.makedirs(settings.USER_LOG_DIR, exist_ok=True)
        with open(os.path.join(settings.USER_LOG_DIR, 'user_visits.txt'), 'a') as f:
            print(post_data, file=f)

    post_fields = json.loads(post_data)
    DEBUG_LOGGER.info(post_fields)

    response = requests.post(LOG_USER_VISITS_URL, json=post_fields)
    return response.text


'''
API views
'''

@csrf_exempt
def api_users_get_json(request):
    ''' GET all users '''
    users = User.objects.all().values()
    result = list(users)
    status = 'ok'
    return JsonResponse(result_with_status(result, status), safe=False)

@csrf_exempt
def api_user_get_json(request, user_id=None):
    ''' GET individual user '''
    result, status = {}, 'error'
    try:
        user = User.objects.get(user_id=user_id)
        result = model_to_dict(user)
        status = 'ok'
    except User.DoesNotExist:
        status = 'User not found'
    return JsonResponse(result_with_status(result, status), safe=False)

@csrf_exempt
def api_user_delete(request, user_id=None):
    result, status = {}, 'error'
    try:
        user = User.objects.get(user_id=user_id)
        user.delete(keep_parents=True)
        status = 'ok'
    except User.DoesNotExist:
        status = 'User not found'
    return JsonResponse(result_with_status(result, status), safe=False)

@csrf_exempt
def api_user_create(request):
    result, status = {}, 'error'
    if request.method == "GET":
        status = 'POST required for create'
    elif request.method == "POST":
        user_fields = {field.name for field in User._meta.fields}
        user_fields -= USER_AUTO_FIELDS
        request_fields = set(request.POST.keys())
        if not request_fields.issuperset(USER_REQUIRED_FIELDS):
            status = 'Required fields {} missing'.format(USER_REQUIRED_FIELDS - request_fields)
        else:
            new_user = User.objects.create(pub_date=timezone.now())
            for key, value in request.POST.items():
                if key not in user_fields:
                    continue
                setattr(new_user, key, value)
            new_user.save()
            result = model_to_dict(new_user)
            status = 'ok'
    else:
        status = 'Unknown request'
    return JsonResponse(result_with_status(result, status), safe=False)

@csrf_exempt
def api_user_update(request, user_id=None):
    result, status = {}, 'error'
    if request.method == "GET":
        status = 'POST required for create'
    elif request.method == "POST":
        try:
            user = User.objects.get(user_id=user_id)
            user_fields = {field.name for field in User._meta.fields}
            user_fields -= USER_AUTO_FIELDS
            for key, value in request.POST.items():
                if key not in user_fields:
                    continue
                setattr(user, key, value)
            user.save()
            result = model_to_dict(user)
            status = 'ok'
        except User.DoesNotExist:
            status = 'User not found'
    else:
        status = 'Unknown request'
    return JsonResponse(result_with_status(result, status), safe=False)


@csrf_exempt
def api_record_user(request):
    result, status = {}, 'error'
    if request.method == "GET":
        status = 'POST required for record_user'
    elif request.method == "POST":
        post_data = OrderedDict()
        post_data['timestamp'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        client_ip = get_client_ip(request)
        if client_ip:
            post_data['client_ip'] = client_ip
        user_agent = request.META['HTTP_USER_AGENT']
        if user_agent:
            post_data['userAgent'] = user_agent

        post_items = list(request.POST.items())
        if not post_items:
            post_items = json.loads(request.body.decode('utf-8')).items()
            # DEBUG_LOGGER.info(post_items)

        for key, value in sorted(post_items):
            post_data[key] = value
        
        result = log_user_visit(json.dumps(post_data))
        result = ''
        status = 'ok'
    else:
        status = 'Unknown request'

    return JsonResponse(result_with_status(result, status), safe=False)

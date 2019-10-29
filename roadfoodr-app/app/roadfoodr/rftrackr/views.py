from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rftrackr.models import User, Roadfood, Visit


def index(request):
    return render(request, 'index.html')


'''
API views and utility functions
'''

def result_with_status(result=None, status=None):
    ''' utility function to add status message to result structure '''
    response = {}
    response['status'] = status
    response['result'] = result if result else {}
    return response

USER_REQUIRED_FIELDS = {'name_first', 'name_last'}
USER_AUTO_FIELDS = {'user_id'}


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





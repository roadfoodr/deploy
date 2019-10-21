from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict

from rftrackr.models import User, Roadfood, Visit

# Create your views here.
def index(request):
    return render(request, 'index.html')


def users_get_json(request, user_id=None):
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
            response = model_to_dict(user)
        # except DoesNotExist:
        except:
            response = {}
    else:
        users = User.objects.all().values()
        response = list(users)
    return JsonResponse(response, safe=False)


def user_delete(request, user_id=None):
    try:
        user = User.objects.get(user_id=user_id)
        user.delete(keep_parents=True)
        response = {'ok': True}
    # except DoesNotExist:
    except:
        response = {'ok': False}
    return JsonResponse(response, safe=False)


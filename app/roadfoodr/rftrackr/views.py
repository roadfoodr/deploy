from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_get_json(request):
    users = User.objects.all().values()
    users_list = list(users)
    json_object = {k: v for k, v in users_list[0]}
    return JsonResponse(json_object)

def users_get_json(request):
    users = User.objects.all().values()
    users_list = list(users)
    json_object = {k: v for k, v in users_list[0]}
    return JsonResponse(users_list, safe=False)

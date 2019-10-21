from django.contrib import admin

# Register your models here.
from .models import User
from .models import Visit
from .models import Roadfood

admin.site.register(User)
admin.site.register(Visit)
admin.site.register(Roadfood)
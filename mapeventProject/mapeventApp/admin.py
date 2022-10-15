from django.contrib import admin
from mapeventApp.models import  Event, Login,AddEvent,Staff,Add
from mapeventApp.models import Sign
from mapeventApp.models import ChangePassword
# Register your models here.
admin.site.register(Login)
admin.site.register(Event)
admin.site.register(AddEvent)
admin.site.register(Staff)
admin.site.register(Add)


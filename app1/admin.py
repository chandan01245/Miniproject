from django.contrib import admin

from .models import appointment, medicine, register

# Register your models here.
admin.site.register(register)
admin.site.register(medicine)
admin.site.register(appointment)
from django.contrib import admin
from .models import Doctor, UserProfile, Appointment

# Register your models here.
admin.site.register(Doctor)
admin.site.register(UserProfile)
admin.site.register(Appointment)
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(AnonymousPersonalData)
admin.site.register(Order)
admin.site.register(Order_detail)
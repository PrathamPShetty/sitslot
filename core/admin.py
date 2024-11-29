from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Event)
admin.site.register(places)
admin.site.register(venue)
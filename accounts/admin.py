from django.contrib import admin
from .models import stack
from .models import cashEntry

admin.site.register(cashEntry)
admin.site.register(stack)

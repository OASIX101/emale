from django.contrib import admin
from .models import MealList, ComUserChoice

# Register your models here.
admin.site.register([MealList,ComUserChoice])
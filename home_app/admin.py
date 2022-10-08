from django.contrib import admin
from .models import MealList, ComUserChoice, VendorMeal

# Register your models here.
@admin.register(MealList)
class ItemAdmin(admin.ModelAdmin):
    list_display_links = ('meal_id_1','meal_id_2','meal_id_3')
    list_display = ('meal_id_1','meal_id_2','meal_id_3')
    list_filter = ('meal_id_1','meal_id_2','meal_id_3', 'day', 'day_num', 'month', 'year')
    search_fields = ('day', 'day_num', 'month', 'year')

@admin.register(ComUserChoice)
class ItemAdmin(admin.ModelAdmin):
    list_display_links = ('user',)
    list_display = ('meal_list', 'meal_order', 'user')
    list_filter = ('meal_list', 'meal_order', 'user',  'day', 'day_num', 'month', 'year')
    search_fields = ('meal_list', 'meal_order', 'user')

@admin.register(VendorMeal)
class ItemAdmin(admin.ModelAdmin):
    list_display_links = ('meal',)
    list_display = ('meal', 'price')
    list_filter = ('meal', 'price', 'day', 'day_num', 'month', 'year')
    search_fields = ('day', 'day_num', 'month', 'year')
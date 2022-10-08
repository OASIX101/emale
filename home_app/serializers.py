from rest_framework import serializers
from .models import MealList, ComUserChoice, VendorMeal

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorMeal
        fields = '__all__'


class VendorSerializer2(serializers.ModelSerializer):

    class Meta:
        model = VendorMeal
        fields = ['id', 'meal', 'price', 'image']

class MealListSerializer(serializers.ModelSerializer):

    class Meta:
        model = MealList
        fields = ['meal_id_1', 'meal_id_2', 'meal_id_3']

class MealListSerializer3(serializers.ModelSerializer):
    meal_1 = serializers.ReadOnlyField()
    meal_2 = serializers.ReadOnlyField()
    meal_3 = serializers.ReadOnlyField()

    class Meta:
        model = MealList
        fields = ['id', 'meal_id_1', 'meal_1', 'meal_id_2', 'meal_2', 'meal_id_3', 'meal_3', 'time_added']

class MealListSerializer2(serializers.ModelSerializer):

    class Meta:
        model = MealList
        fields = '__all__'

class MealOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComUserChoice
        fields = ['meal_order']

class MealOrderSerializer2(serializers.ModelSerializer):

    class Meta:
        model = ComUserChoice
        fields = '__all__'

class MealOrderSerializer3(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField()
    user_info = serializers.ReadOnlyField()
 
    class Meta:
        model = ComUserChoice
        fields = ['id', 'meal_order', 'meal_list', 'meal', 'user', 'user_info', 'time_order']

class MealOrderSerializer4(serializers.ModelSerializer):
    meal = serializers.ReadOnlyField()

    class Meta:
        model = ComUserChoice
        fields = ['id','day_num', 'meal_order', 'meal']


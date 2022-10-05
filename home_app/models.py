from django.db import models
from django.forms import model_to_dict
from home_accounts.models import CustomUser

class VendorMeal(models.Model):
    meal = models.CharField(max_length=255, unique=True)
    price = models.FloatField(default=0.0)
    day = models.CharField(max_length=100) 
    day_num = models.IntegerField()
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100) 
    time_added = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.meal

class MealList(models.Model):

    meal_id_1 = models.ForeignKey(VendorMeal, related_name="meal_1", on_delete=models.CASCADE)
    meal_id_2 = models.ForeignKey(VendorMeal, related_name="meal_2", on_delete=models.CASCADE)
    meal_id_3 = models.ForeignKey(VendorMeal, related_name="meal_3", on_delete=models.CASCADE)
    day = models.CharField(max_length=100) 
    day_num = models.IntegerField()
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100) 
    time_added = models.TimeField(auto_now_add=True, null=True)
 
    @property
    def meal_1(self):
        return model_to_dict(self.meal_id_1, fields=['meal'])
    @property
    def meal_2(self):
        return model_to_dict(self.meal_id_2, fields=['meal'])
    @property
    def meal_3(self):
        return model_to_dict(self.meal_id_3, fields=['meal'])

    def __str__(self):
        return f'{self.day_num}-{self.month}-{self.year}'

class ComUserChoice(models.Model):

    meal_list = models.ForeignKey(MealList, related_name="meal_list", on_delete=models.CASCADE)
    meal_order = models.ForeignKey(VendorMeal, related_name="meal_order", on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="users", on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    day_num = models.IntegerField()
    month = models.CharField(max_length=100)
    year = models.CharField(max_length=100) 
    time_order = models.TimeField(auto_now_add=True)

    @property
    def meal(self):
        return model_to_dict(self.meal_order, fields=['meal'])
    @property
    def user_info(self):
        return model_to_dict(self.user, fields=['username', 'gender'])

    def __str__(self):
        return self.meal_order

     



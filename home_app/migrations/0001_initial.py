# Generated by Django 4.1.1 on 2022-10-08 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(max_length=255, unique=True)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.ImageField(upload_to='MealImages/%Y/%m/%d/')),
                ('day', models.CharField(max_length=100)),
                ('day_num', models.IntegerField()),
                ('month', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('time_added', models.TimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=100)),
                ('day_num', models.IntegerField()),
                ('month', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('time_added', models.TimeField(auto_now_add=True, null=True)),
                ('meal_id_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_1', to='home_app.vendormeal')),
                ('meal_id_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_2', to='home_app.vendormeal')),
                ('meal_id_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_3', to='home_app.vendormeal')),
            ],
        ),
        migrations.CreateModel(
            name='ComUserChoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=100)),
                ('day_num', models.IntegerField()),
                ('month', models.CharField(max_length=100)),
                ('year', models.CharField(max_length=100)),
                ('time_order', models.TimeField(auto_now_add=True)),
                ('meal_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_list', to='home_app.meallist')),
                ('meal_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_order', to='home_app.vendormeal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

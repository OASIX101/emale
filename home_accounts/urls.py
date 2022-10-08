from django.urls import path, include
from . import views

urlpatterns = [
    path('user/', views.CreateUser().as_view(), name='create-user'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-edit/<int:user_id>/', views.UserEdit().as_view(), name='user-edit'),
    path('staff-vendor/', views.get_staff_vendor, name='get-staff-vendor'),
    path('activate/<int:user_id>/', views.activate, name='activate'),
    path('', include('djoser.urls'))
]
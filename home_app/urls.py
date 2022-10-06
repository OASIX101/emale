from django.urls import path
from . import views

urlpatterns = [
    path('meal-list/', views.MealListView().as_view(), name='meal-list'),
    path('meal-order/', views.MealOrderView().as_view(), name='meal-order'),
    path('vendor-edit/<int:item_id>/', views.VendorListEdit().as_view(), name='vendor-edit'),
    path('vendor-meal/', views.VendorListView.as_view(), name='vendor-meal'),
    path('all-orders/', views.get_all_order, name='pending-meal'),
    path('view-user-history/<int:user_id>/<str:month>/<int:year>/', views.UserMonthlyHistoryAdmin.as_view(), name='user_history'),
    path('user-history/<str:month>/<int:year>/', views.UserMonthlyHistory.as_view(), name='user_loggedin_history'),
]
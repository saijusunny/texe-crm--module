from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('users_lst',views.users_lst, name='users_lst'),
    path('staff_home',views.staff_home, name='staff_home'),
    path('ser_cmp',views.ser_cmp, name='ser_cmp'),
    path('add_complaint',views.add_complaint, name='add_complaint'),
    path('add_user_complaint',views.add_user_complaint, name='add_user_complaint'),
    path('add_service',views.add_service, name='add_service'),
    path('add_user_service',views.add_user_service, name='add_user_service'),
    
    path('registration',views.registration, name='registration'),


    path('icons',views.icons, name='icons'),
]

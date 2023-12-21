from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name='login'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('users',views.users, name='users'),

    path('registration',views.registration, name='registration'),


    path('icons',views.icons, name='icons'),
]

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
    path('add_staff',views.add_staff, name='add_staff'),
    path('edit_staff/<int:id>',views.edit_staff, name='edit_staff'),
    path('save_edit_staff/<int:id>',views.save_edit_staff, name='save_edit_staff'),
    path('delete_staff/<int:id>',views.delete_staff, name='delete_staff'),
    path('orders_dta',views.orders_dta, name='orders_dta'),

    path('all_events',views.all_events, name='all_events'),
    path('add_event',views.add_event, name='add_event'),
    path('update',views.update, name='update'),
    path('remove',views.remove, name='remove'),
    path('get_date_event',views.get_date_event, name='get_date_event'),
    path('view_items_orders',views.view_items_orders, name='view_items_orders'),

    
    
    #########################################################################Staff Module
    path('staff_index',views.staff_index, name='staff_index'),
    path('registrations',views.registrations, name='registrations'),
    path('icons',views.icons, name='icons'),

    ######################################################################################
    path('logout',views.logout, name='logout'),

    
]

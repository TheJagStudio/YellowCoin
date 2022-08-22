from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('cash_ledge/', views.cash_ledge, name='cash_ledge'),
    path('cash_entry/', views.cash_entry, name='cash_entry'),
    path('jv/', views.jv, name='jv'),
    path('jv_broker/', views.jv_broker, name='jv_broker'),
    path('jv_broker_delete/', views.jv_broker_delete, name='jv_broker_delete'),
    path('deposit_entry/', views.deposit_entry, name='deposit_entry'),
    path('valan/', views.valan, name='valan'),
]

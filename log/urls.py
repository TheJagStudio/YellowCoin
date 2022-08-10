from django.urls import path
from . import views

app_name = 'log'
urlpatterns = [
    path('', views.trade_edit, name='trade_edit'),
    path('user_log/', views.user_log, name='user_log'),
    path('auto/', views.auto, name='auto'),
    path('cross_log/', views.cross_log, name='cross_log'),
    path('rejection_log/', views.rejection_log, name='rejection_log'),
]

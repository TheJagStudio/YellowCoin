from django.urls import path

from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('running_orders/', views.running_orders, name='running_orders'),
    path('exected_orders/', views.exected_order, name='exected_order'),
    path('summary_reports/', views.summary_reports, name='summary_reports'),
    path('trade_entry/', views.trade_entry, name='trade_entry'),
    path('M2M_alerts/', views.M2M, name='M2M'),
    path('user/', views.user, name='user'),
]

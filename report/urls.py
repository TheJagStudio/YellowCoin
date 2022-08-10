from django.urls import path
from . import views

app_name = 'report'
urlpatterns = [
    path('', views.track_report, name='track_report'),
    path('ledge_report/', views.ledge_report, name='ledge_report'),
    path('deposit_report/', views.deposit_report, name='deposit_report'),
    path('trail_report/', views.trail_report, name='trail_report'),
    path('client_report/', views.client_report, name='client_report'),
]

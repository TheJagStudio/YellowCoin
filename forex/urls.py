from django.urls import path

from . import views
app_name = 'forex'
urlpatterns = [
    path('', views.forex_wacthlist, name='forex_wacthlist'),
    path('trades/', views.forex_trades, name='forex_trades'),
    path('portfolio/', views.forex_portfolio, name='forex_portfolio'),
    path('margin/', views.forex_margin, name='forex_margin'),
]

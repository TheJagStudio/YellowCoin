from django.urls import path

from . import views
app_name = 'user'
urlpatterns = [
    path('adduser/', views.adduser, name='adduser'),
    path('user_list/', views.user_list, name='user_list'),
]

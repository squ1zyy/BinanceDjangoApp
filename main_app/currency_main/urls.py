from django.urls import path
from .views import *
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', main_page, name='main-page'),
    path('currency_graphics/', graphics, name='graphics-page'),
    path('item-list/', update_binance_data, name='item_list'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'), 
]
from django.urls import path
from .views import *
from django.contrib.auth import views as authViews

urlpatterns = [
    path('', main_page, name='main-page'),
    path('currency_graphics/', currency_converter, name='graphics-page'),
    path('item-list/', update_binance_data, name='item_list'),
    path('profile/', profile, name='profile'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  
        activate, name='activate'), 
    path('get_last_price/', last_price, name='get_last_price'),
    path('delete/<int:id>/', delete, name='delete'),
    path('edit/<int:id>/', edit, name='edit'),

    # path('1', trade_view, name='1'),
    # path('convert_currency/', currency_converter, name='convert_currency'),
]
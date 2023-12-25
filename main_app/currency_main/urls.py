from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main-page'),
    path('currency_graphics/', graphics, name='graphics-page'),
]
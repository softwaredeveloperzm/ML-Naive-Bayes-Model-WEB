from django.urls import path
from app.views import *

urlpatterns = [
    path('', news, name="new"),
    path('app', home, name="home"),  
    path('app/category/<str:i>', category, name="category"),
    path('app/setup', setup, name="setup")
]

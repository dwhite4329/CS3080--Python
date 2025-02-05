from django.urls import path
from . import views

urlpatterns = [
    path('weather/<str:city>/<str:state>/<str:country>/', views.weather, name='weather')
]
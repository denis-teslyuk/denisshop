from django.urls import path

from denisshop import views

urlpatterns = [
    path('', views.index, name='home')
]
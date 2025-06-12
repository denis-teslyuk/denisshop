from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns =[
    path('add-item/<slug:slug>/', views.add_item, name='add_item')
]
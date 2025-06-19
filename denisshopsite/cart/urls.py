from django.urls import path

from cart import views

app_name = 'cart'

urlpatterns =[
    path('add-item/<slug:slug>/', views.add_item, name='add_item'),
    path('delete-item/<slug:slug>/', views.delete_item, name='delete_item'),
    path('delete-item/', views.delete_item, name='delete_item'),
    path('show_cart/', views.show_cart, name='show_cart')
]
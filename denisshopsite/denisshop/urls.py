from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add-review/<slug:slug>/', views.add_review, name='add_review')
]
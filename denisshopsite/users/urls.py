from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrationUser.as_view(), name='registration'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('password-change/', PasswordChangeView.as_view(template_name = "users/password_change_form.html",
         success_url = reverse_lazy("users:password_change_done")),name='password_change'),
    path('password-change-done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
]
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import RegistrationForm


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    extra_context = {'title':'Авторизация'}
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    extra_context = {'title':'Регистрация'}

    def get_success_url(self):
        return reverse_lazy('home')
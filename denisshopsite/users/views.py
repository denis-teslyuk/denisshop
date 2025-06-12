from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from cart.models import Cart
from users.forms import RegistrationForm, ProfileForm


# Create your views here.
class LoginUser(LoginView):
    form_class = AuthenticationForm
    extra_context = {'title':'Авторизация'}
    template_name = 'users/login.html'


class RegistrationUser(CreateView):
    form_class = RegistrationForm
    template_name = 'users/registration.html'
    extra_context = {'title':'Регистрация'}

    def get_success_url(self):
        return reverse_lazy('home')


class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'Профиль'}

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)


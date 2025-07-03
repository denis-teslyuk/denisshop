from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from cart.models import Cart
from denisshop.models import Key
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        context['keys'] = Key.objects.filter(user = self.request.user).select_related('game', 'review')
        return context

    def get_object(self, queryset=None):
        return get_user_model().objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('users:profile')


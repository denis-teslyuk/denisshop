from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя или E-mail')
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повтор пароля')

    class Meta:
        model = get_user_model()
        fields = ['username','email', 'first_name', 'last_name', 'password1','password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email = email):
            raise ValidationError('Пользователь с таким E-mail же существует')
        return email
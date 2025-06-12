from django.contrib.auth import get_user_model
from django.db import models

from denisshop.models import Game


# Create your models here.
class Cart(models.Model):
    games = models.ManyToManyField(Game, related_name='cart',verbose_name='Игры')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                related_name='cart', verbose_name='Пользователь')

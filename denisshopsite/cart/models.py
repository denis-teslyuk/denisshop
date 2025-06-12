from django.contrib.auth import get_user_model
from django.db import models

from denisshop.models import Game


# Create your models here.
class Cart(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='cart',verbose_name='Игры')
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE,
                                related_name='cart', verbose_name='Пользователь')
    amount = models.PositiveIntegerField(verbose_name='Количество', default=1)

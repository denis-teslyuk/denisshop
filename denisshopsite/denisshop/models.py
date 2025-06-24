from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Game(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    slug = models.SlugField(max_length=256,blank=True, unique=True, verbose_name='Слаг')
    image = models.ImageField(upload_to='game_images', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    sale_price = models.FloatField(blank=True, null=True, verbose_name='Цена со скидкой')
    processor = models.CharField(max_length=64, verbose_name='Процессор')
    ozu = models.PositiveIntegerField(verbose_name='Оперативная память')
    videocard = models.CharField(verbose_name='Видеокарта')
    hard_space = models.PositiveIntegerField(verbose_name='Жесткий диск')
    platform = models.ManyToManyField('Platform', related_name='games', verbose_name='Платформы')
    genres = models.ManyToManyField('Genre', related_name='games', verbose_name='Жанры')
    series = models.ForeignKey('Series',null=True, on_delete=models.SET_NULL, verbose_name='Серия')
    release = models.DateField(verbose_name='Дата выхода')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game', args=self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Platform(models.Model):
    title = models.CharField(max_length=64, verbose_name='Платформа')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Платформа'
        verbose_name_plural = 'Платформы'


class Genre(models.Model):
    title = models.CharField(max_length=64, verbose_name='Жанр')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Series(models.Model):
    title = models.CharField(max_length=128, verbose_name='Серия игр')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии'


class Key(models.Model):
    key = models.CharField(max_length=64, unique=True, verbose_name='Ключ')
    slug = models.SlugField(max_length=64, blank=True, unique=True)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, verbose_name='Игра', related_name='keys')
    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING,
                             null=True, blank=True, default=None, verbose_name='Владелец')

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        self.slug = slugify(self.key)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'


class Review(models.Model):
    content = models.TextField(verbose_name='Содержание')
    key = models.OneToOneField('Key', on_delete=models.CASCADE, null=True,
                               blank=True, related_name='review')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


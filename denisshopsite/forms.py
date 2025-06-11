from django import forms

from denisshop.models import Genre, Series, Platform


class FilterForm(forms.Form):
    SORT_CHOICES = (
        ('-release', 'Дата выхода, по убыванию'),
        ('release', 'Дата выхода, по возрастаниюе'),
        ('percent', 'По скидке'),
        ('-price', 'Цена, по убыванию'),
        ('price', 'Цена, по возрастанию'),
        ('-title', 'Название, по убыванию'),
        ('title', 'Название, по возрастанию'),

    )
    min_price = forms.FloatField(required=False, label='от')
    max_price = forms.FloatField(required=False, label='до')
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, label='Жанр')
    platform = forms.ModelMultipleChoiceField(queryset=Platform.objects.all(),required=False, label='Платформа')
    series = forms.ModelMultipleChoiceField(queryset=Series.objects.all(),required=False, label='Серия')
    sort = forms.ChoiceField(choices=SORT_CHOICES,required=False, label='Сортировка')

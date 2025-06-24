from django import forms

from denisshop.models import Genre, Series, Platform, Review


class FilterForm(forms.Form):
    SORT_CHOICES = (
        ('-release', 'Дата выхода, по убыванию'),
        ('release', 'Дата выхода, по возрастанию'),
        ('percent', 'По скидке'),
        ('-price', 'Цена, по убыванию'),
        ('price', 'Цена, по возрастанию'),
        ('-title', 'Название, по убыванию'),
        ('title', 'Название, по возрастанию'),

    )
    min_price = forms.FloatField(required=False, label='от: ',
                                 widget=forms.NumberInput(attrs = {'class':'index-aside-price'}))
    max_price = forms.FloatField(required=False, label='до: ',
                                 widget=forms.NumberInput(attrs = {'class':'index-aside-price'}))
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), required=False, label='Жанр',
                                            widget=forms.SelectMultiple(attrs = {'class':'index-aside-filter'}))
    platform = forms.ModelMultipleChoiceField(queryset=Platform.objects.all(),required=False, label='Платформа',
                                              widget=forms.SelectMultiple(attrs = {'class':'index-aside-filter'}))
    series = forms.ModelMultipleChoiceField(queryset=Series.objects.all(),required=False, label='Серия',
                                            widget=forms.SelectMultiple(attrs = {'class':'index-aside-filter'}))
    sort = forms.ChoiceField(choices=SORT_CHOICES,required=False, label='Сортировка',
                             widget=forms.Select(attrs = {'class':'index-aside-sort'}))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'add-review-form'})}
        labels = {'content':''}
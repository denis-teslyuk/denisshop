from django import forms

from denisshop.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']
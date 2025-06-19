from django.db.models import F
from django.shortcuts import render, redirect

from cart.models import Cart
from denisshop.models import Game


# Create your views here.
def add_item(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except:
        return redirect(request.META.get('HTTP_REFERER'))
    try:
        item = Cart.objects.get(game=game, user=request.user)
    except:
        Cart.objects.create(game=game, user=request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    item.amount = F('amount') + 1
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def delete_item(request, slug):
    if request.GET.get('count') == 'all':
        Cart.objects.filter(user=request.user).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    Cart.objects.filter(game__slug = slug, user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER'))



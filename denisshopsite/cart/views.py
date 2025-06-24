from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect

from cart.models import Cart
from denisshop.models import Game, Key


# Create your views here.
@login_required
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


@login_required
def delete_item(request, slug=None):
    if request.GET.get('count') == 'all':
        Cart.objects.filter(user=request.user).delete()
        return redirect(request.META.get('HTTP_REFERER'))

    try:
        item = Cart.objects.get(game__slug=slug, user=request.user)
    except:
        return redirect(request.META.get('HTTP_REFERER'))

    if request.GET.get('count') == '1':
        if item.amount == 1:
            item.delete()
            return redirect(request.META.get('HTTP_REFERER'))
        item.amount = F('amount') - 1
        item.save()
    else:
        item.delete()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def show_cart(request):
    item_list = Cart.objects.filter(user = request.user)
    data = {'item_list':item_list, 'title':'Корзина'}
    return render(request, 'cart/show_cart.html', data)


@login_required
def buy_items(request):
    item_list = Cart.objects.filter(user = request.user)
    for item in item_list:
        if item.amount > item.game.keys.filter(user=None).count():
            return redirect(request.META.get('HTTP_REFERER'))
    #Здесь мог бы быть код для оплаты
    for item in item_list:
        keys = Key.objects.filter(game = item.game)[:item.amount]
        for key in keys:
            key.user = request.user
            key.save()
        item.delete()
    return redirect(request.META.get('HTTP_REFERER'))




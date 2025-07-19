from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from cart.models import Cart
from cart.utils import get_count_free_keys, delete_one, mark_purchased, handle_add
from denisshop.models import Game


# Create your views here
@login_required
def add_item(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except:
        return redirect(request.META.get('HTTP_REFERER', '/'))

    handle_add(request, game)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def delete_item(request, slug=None):
    if request.GET.get('count') == 'all':
        Cart.objects.filter(user=request.user).delete()
    else:
        try:
            item = Cart.objects.get(game__slug=slug, user=request.user)
        except:
            return redirect(request.META.get('HTTP_REFERER', '/'))
        delete_one(request, item)

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def show_cart(request):
    item_list = Cart.objects.filter(user = request.user).select_related('game')

    count_free_keys_by_game = get_count_free_keys()
    for item in item_list:
        item.free_count = count_free_keys_by_game.get(item.game_id, 0)

    data = {'item_list':item_list, 'title':'Корзина'}
    return render(request, 'cart/show_cart.html', data)


@login_required
def buy_items(request):
    item_list = Cart.objects.filter(user = request.user)

    num_free_keys_by_game = get_count_free_keys()
    for item in item_list:
        if item.amount > num_free_keys_by_game[item.game_id]:
            return redirect(request.META.get('HTTP_REFERER', '/'))

    #Здесь мог бы быть код для оплаты

    mark_purchased(request.user, item_list)

    return redirect(request.META.get('HTTP_REFERER', '/'))




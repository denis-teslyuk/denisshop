from django.db.models import Count, F
from cart.models import Cart
from denisshop.models import Key


def handle_add(request, game):
    try:
        item = Cart.objects.get(game=game, user=request.user)
    except:
        Cart.objects.create(game=game, user=request.user)
    else:
        item.amount = F('amount') + 1
        item.save()


def get_count_free_keys():
    count_free_keys = Key.objects.filter(user__isnull=True).values('game_id').annotate(free_count=Count('game_id'))
    return {k['game_id']: k['free_count'] for k in count_free_keys}


def delete_one(request, item):
    if item.amount == 1 or 'count' not in request.GET:
        item.delete()
    else:
        item.amount = F('amount') - 1
        item.save()


def mark_purchased(user, item_list):
    for item in item_list:
        keys = Key.objects.filter(game = item.game)[:item.amount]
        for key in keys:
            key.user = user
            key.save()
        item.delete()


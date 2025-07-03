from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F


def filter_games(get_dict, queryset):
    for key in get_dict:
        if key in ('genres', 'platform', 'series'):
            lookup = f'{key}__id__in'
            arg_list = filter(lambda x: x.isdigit(),get_dict.getlist(key))
            queryset = queryset.filter(**{lookup : arg_list}).distinct()

    return queryset


def sort_games(get_dict, queryset):
    if get_dict['sort'] == 'percent':  # Сортировка по проценту скидки
        calc_sale = lambda a, b: (1 - a/b) * 100
        queryset = queryset.annotate(percent=calc_sale(F('sale_price'), F('price'))
                                      if F('sale_price') is not None else 0)

    PARAM_NAMES = ('price', '-price', 'title', '-title', 'release', '-release', 'percent')
    if get_dict['sort'] in PARAM_NAMES:  # Сортировка по полям
        queryset = queryset.order_by(get_dict['sort'])

    return queryset


def filter_price(get_dict, queryset):
    check_price = lambda x: x is not None and x.isdigit()
    min_price = get_dict.get('min_price') if check_price(get_dict.get('min_price')) else 0
    max_price = get_dict.get('max_price') if check_price(get_dict.get('max_price')) else 1000000
    queryset = queryset.filter(price__gte = min_price, price__lte = max_price)
    return queryset


def filter_all(request, games):
    games = games.filter(sale_price__isnull=False) if 'sale' in request.GET else games

    games = filter_price(request.GET, games)
    games = filter_games(request.GET, games)

    return games.filter(title__contains=request.GET.get('search', ''))


def add_amount_field(cart_items, games):
    cart_items = {item.game_id: item.amount for item in cart_items}
    for game in games:
        game.amount = cart_items.get(game.pk, 0)
from django.db.models import F


def filter_games(get_dict, queryset):
    for key in get_dict:
        if key in ('genres', 'platform', 'series'):
            lookup = f'{key}__id__in'
            arg_list = get_dict.getlist(key)
            queryset = queryset.filter(**{lookup : arg_list}).distinct()

    return queryset


def sort_games(get_dict, queryset):
    if get_dict['sort'] == 'percent':  # Сортировка по проценту скидки
        calc_sale = lambda a, b: (1 - a/b) * 100
        queryset = queryset.annotate(percent=calc_sale(F('sale_price'), F('price'))
                                      if F('sale_price') is not None else 0)
        queryset = queryset.order_by('percent')

    PARAM_NAMES = ('price', '-price', 'title', '-title', 'release', '-release')
    if get_dict['sort'] in PARAM_NAMES:  # Сортировка по полям
        queryset = queryset.order_by(get_dict['sort'])

    return queryset


def filter_price(get_dict, queryset):
    check_price = lambda x: x is not None and x.isdigit()
    min_price = get_dict.get('min_price') if check_price(get_dict.get('min_price')) else 0
    max_price = get_dict.get('max_price') if check_price(get_dict.get('max_price')) else 1000000
    queryset = queryset.filter(price__gte = min_price, price__lte = max_price)
    return queryset
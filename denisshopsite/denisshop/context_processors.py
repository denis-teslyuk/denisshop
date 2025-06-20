menu = [{'title':'Каталог', 'url_name':'home'},{'title':'Скидки', 'url_name':'home'},
        {'title':'Отзывы', 'url_name':'show_review'},]

def get_menu(request):
    return {'menu':menu}
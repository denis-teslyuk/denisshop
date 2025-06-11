from django.shortcuts import render

from forms import FilterForm
from .utils import filter_games, sort_games, filter_price
from .models import Game


# Create your views here.
def index(request):
    games = Game.objects.all()
    form = FilterForm(request.GET)

    games = games.filter(sale_price__isnull=False) if 'sale' in request.GET else games
    games = games.filter(title__contains=request.GET.get('search', ''))

    games = filter_price(request.GET, games)
    games = filter_games(request.GET, games)
    games = sort_games(request.GET, games) if 'sort' in request.GET else games

    data = {
        'games': games,
        'form':form
    }
    return render(request, 'denisshop/index.html', data)



from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from forms import FilterForm
from .forms import ReviewForm
from .utils import filter_games, sort_games, filter_price
from .models import Game, Key, Review


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


def add_review(request, slug):
    try:
        key = Key.objects.get(slug = slug, user = request.user, review=None)
    except ObjectDoesNotExist:
        return redirect('home')
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rev = form.save(commit=False)
            rev.key = key
            rev.save()
            return redirect('users:profile')

    form = ReviewForm()
    return render(request, 'denisshop/add_review.html', {'title':'Отзыв', 'form':form})


def show_review(request):
    if request.GET.get('choice') == 'my':
        review_list = Review.objects.filter(key__user = request.user)
    else:
        review_list = Review.objects.all()
    data = {
        'title':'Отзывы',
        'review_list':review_list
    }
    return render(request, 'denisshop/show_review.html', data)
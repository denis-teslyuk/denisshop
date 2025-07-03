from time import time

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Value
from django.shortcuts import render, redirect

from cart.models import Cart
from .forms import ReviewForm, FilterForm
from .utils import sort_games, filter_all
from .models import Game, Key, Review


# Create your views here.
def index(request):
    games = filter_all(request, Game.objects.all().prefetch_related('genres'))
    games = sort_games(request.GET, games) if 'sort' in request.GET else games

    cart_items = {item.game_id:item.amount for item in Cart.objects.filter(user = request.user)}
    for game in games:
        game.amount = cart_items.get(game.pk, 0)


    form = FilterForm(request.GET)
    data = {'games': games,'form':form}

    return render(request, 'denisshop/index.html', data)


def show_game(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return redirect('home')

    try:
        game.amount = request.user.cart.get(game = game).amount
    except ObjectDoesNotExist:
        game.amount = 0

    data = {
        'game':game,
        'title': game.title,
        'game_series': Game.objects.filter(~Q(slug = game.slug),series=game.series),
        'reviews': Review.objects.filter(key__game = game)
    }
    return render(request, 'denisshop/game.html', data)


@login_required
def add_review(request, slug):
    try:
        key = Key.objects.get(slug = slug, user = request.user, review=None)
    except ObjectDoesNotExist:
        return redirect('home')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.key = key
            review.save()
            return redirect('users:profile')

    form = ReviewForm()
    data = {
        'title': 'Отзыв',
        'form': form,
        'game': key.game,
    }
    return render(request, 'denisshop/add_review.html', data)


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

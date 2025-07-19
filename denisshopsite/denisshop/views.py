from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render, redirect

from cart.utils import get_count_free_keys
from .forms import ReviewForm, FilterForm
from .utils import sort_games, filter_all, add_amount_field, get_page
from .models import Game, Key, Review


# Create your views here.
def index(request):
    games = filter_all(request, Game.objects.filter(keys__user__isnull = True).distinct().prefetch_related('genres'))
    games = sort_games(request.GET, games) if 'sort' in request.GET else games

    if request.user.is_authenticated:
        add_amount_field(request.user.cart.all(), games)

    page = get_page(request, games)

    form = FilterForm(request.GET)
    data = {'page': page,'form':form}

    return render(request, 'denisshop/index.html', data)


def show_game(request, slug):
    try:
        game = Game.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return redirect('home')

    if request.user.is_authenticated:
        add_amount_field(request.user.cart.all(), [game])

    game.free_keys = get_count_free_keys().get(game.pk, 0)

    data = {
        'game':game,
        'title': game.title,
        'game_series': Game.objects.filter(~Q(slug = game.slug),series=game.series).prefetch_related('keys'),
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
        review_list = Review.objects.filter(key__user = request.user).select_related('key', 'key__user')
    else:
        review_list = Review.objects.all().select_related('key__user')

    page = get_page(request, review_list)

    data = {'title':'Отзывы','page':page}
    return render(request, 'denisshop/show_review.html', data)

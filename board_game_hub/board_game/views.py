from django.shortcuts import render
from . models import Game
from django.core.paginator import Paginator
from django.shortcuts import render,  get_object_or_404

def index(request):
    num_games = Game.objects.all().count()
    context = {
    'num_games': num_games,
    }

    return render(request, 'board_game/index.html', context)

def game_list(request):
    paginator = Paginator(Game.objects.all(), 3)
    game_list = paginator.get_page(request.GET.get("page"))
    return render(request, 'board_game/game_list.html', {'game_list': game_list})

def game_detail(request, pk: int):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'board_game/game_detail.html', {'game': game})

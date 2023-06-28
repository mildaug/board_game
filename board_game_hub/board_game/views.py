from django.shortcuts import render
from . models import Game

def index(request):
    num_games = Game.objects.all().count()
    context = {
    'num_games': num_games,
    }

    return render(request, 'board_game/index.html', context)

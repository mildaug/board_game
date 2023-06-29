from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Game
from .forms import GameBorrowForm
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    num_games = Game.objects.count()
    context = {
        'num_games': num_games,
    }
    return render(request, 'board_game/index.html', context)

def game_list(request):
    paginator = Paginator(Game.objects.all(), 3)
    page_number = request.GET.get('page')
    game_list = paginator.get_page(page_number)
    return render(request, 'board_game/game_list.html', {'game_list': game_list})

def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'board_game/game_detail.html', {'game': game})

@login_required
def borrow_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = GameBorrowForm(request.POST)
        if form.is_valid():
            return render(request, 'board_game/success.html')
    else:
        form = GameBorrowForm()

    return render(request, 'board_game/borrow_game.html', {'game': game, 'form': form})


class UserGameListView(LoginRequiredMixin, ListView):
    template_name = 'board_game/user_game_list.html'
    context_object_name = 'game_list'
    paginate_by = 3

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user)
    
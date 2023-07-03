from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Game, Publisher, GameBorrowRequest, GameRating
from .forms import GameBorrowForm, GameBorrowRequestStatusForm, GameRatingForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg


def index(request):
    num_games = Game.objects.count()
    context = {
        'num_games': num_games,
    }
    return render(request, 'board_game/index.html', context)

def game_list(request):
    game_list = Game.objects.order_by('-rating')
    paginator = Paginator(game_list, 15)
    page_number = request.GET.get('page')
    game_list = paginator.get_page(page_number)
    return render(request, 'board_game/game_list.html', {'game_list': game_list})

@login_required
def game_detail(request, pk):
    game = get_object_or_404(Game, pk=pk)
    ratings = GameRating.objects.filter(game=game)
    average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    user_rated = ratings.filter(user=request.user).exists()

    if request.method == 'POST' and not user_rated:
        form = GameRatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']
            game_rating = GameRating(game=game, user=request.user, rating=rating, comment=comment)
            game_rating.save()
            average_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            game.rating = average_rating
            game.save()
            user_rated = True
    else:
        form = GameRatingForm()

    return render(request, 'board_game/game_detail.html', {'game': game, 'form': form, 'ratings': ratings, 'average_rating': average_rating, 'user_rated': user_rated})

@login_required
def borrow_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = GameBorrowForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.game = game
            borrow_request.borrower = request.user
            borrow_request.owner = game.owner
            borrow_request.save()
            messages.success(request, 'Borrow request submitted successfully.')
            return redirect('game_detail', pk=game_id)
    else:
        form = GameBorrowForm()

    return render(request, 'board_game/borrow_game.html', {'game': game, 'form': form})


class UserGameListView(LoginRequiredMixin, ListView):
    template_name = 'board_game/user_game_list.html'
    context_object_name = 'game_list'
    paginate_by = 3

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user)
    

class GameBorrowRequestListView(LoginRequiredMixin, ListView):
    model = GameBorrowRequest
    template_name = 'board_game/game_borrow_request_list.html'
    context_object_name = 'game_borrow_requests'

    def get_queryset(self):
        return GameBorrowRequest.objects.filter(owner=self.request.user)
    

class GameBorrowRequestDetailView(DetailView):
    model = GameBorrowRequest
    template_name = 'board_game/game_borrow_request_detail.html'
    context_object_name = 'game_borrow_request'

def accept_game_borrow_request(request, pk):
    game_borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)

    if request.method == 'POST':
        form = GameBorrowRequestStatusForm(request.POST, instance=game_borrow_request)
        if form.is_valid():
            form.instance.is_accepted = True
            form.save()
            return redirect('game_borrow_request_detail', pk=pk)
    else:
        form = GameBorrowRequestStatusForm(instance=game_borrow_request)

    return render(request, 'board_game/accept_game_borrow_request.html', {'form': form})

def decline_game_borrow_request(request, pk):
    game_borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)

    if request.method == 'POST':
        form = GameBorrowRequestStatusForm(request.POST, instance=game_borrow_request)
        if form.is_valid():
            form.instance.is_accepted = False
            form.save()
            return redirect('game_borrow_request_detail', pk=pk)
    else:
        form = GameBorrowRequestStatusForm(instance=game_borrow_request)

    return render(request, 'board_game/decline_game_borrow_request.html', {'form': form})


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'board_game/publisher_detail.html'
    context_object_name = 'publisher'
    
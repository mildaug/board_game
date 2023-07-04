from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Game, Publisher, GameBorrowRequest, GameRating
from .forms import GameForm, GameRatingForm, BorrowRequestCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from datetime import timedelta
from django.utils import timezone


def index(request):
    games = Game.objects.order_by('-rating')[:3]  
    return render(request, 'board_game/index.html', {'games': games})

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

    return render(request, 'board_game/game_detail.html', {'game': game, 'form': form, 'ratings': ratings, 'average_rating': average_rating, 'user_rated': user_rated, 'video_url': game.video_url})

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user
            game.save()
            return redirect('game_list')
    else:
        form = GameForm()
    return render(request, 'board_game/create_game.html', {'form': form})

@login_required
def update_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        form = GameForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            return redirect(game)
    else:
        form = GameForm(instance=game)
    return render(request, 'board_game/update_game.html', {'form': form, 'game': game})

@login_required
def delete_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    if request.method == 'POST':
        game.delete()
        return redirect('game_list')
    return render(request, 'board_game/delete_game.html', {'game': game})

@login_required
def create_borrow_request(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    
    if request.method == 'POST':
        form = BorrowRequestCreateForm(request.POST)
        if form.is_valid():
            borrow_request = form.save(commit=False)
            borrow_request.borrower = request.user
            borrow_request.owner = game.owner
            borrow_request.game = game
            borrow_request.save()
            return redirect('submited_game_borrow_request_list')
    else:
        form = BorrowRequestCreateForm()
    
    return render(request, 'board_game/game_borrow_request.html', {'form': form, 'game': game})

@login_required
def submited_game_borrow_list(request):
    borrow_requests = GameBorrowRequest.objects.filter(borrower=request.user)
    return render(request, 'board_game/submited_game_borrow_request_list.html', {'borrow_requests': borrow_requests})

@login_required
def received_game_borrow_list(request):
    borrow_requests = GameBorrowRequest.objects.filter(owner=request.user)
    return render(request, 'board_game/received_game_borrow_request_list.html', {'borrow_requests': borrow_requests})

@login_required
def accept_borrow_request(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    borrow_request.accepted = True
    borrow_request.save()
    return redirect('game_borrow_request_detail', pk=borrow_request.pk)

@login_required
def reject_borrow_request(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    borrow_request.delete()
    return redirect('game_borrow_request_list')

@login_required
def extend_due_date(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    days = 7
    if borrow_request.due_back:
        new_due_back = borrow_request.due_back + timedelta(days=days)
    else:
        new_due_back = timezone.now().date() + timedelta(days=days)
    borrow_request.due_back = new_due_back
    borrow_request.save()
    return redirect('game_borrow_request_detail', pk=borrow_request.pk)

@login_required
def mark_as_returned(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    borrow_request.returned = True
    borrow_request.save()
    return redirect('game_borrow_request_detail', pk=borrow_request.pk)


class UserGameListView(LoginRequiredMixin, ListView):
    template_name = 'board_game/user_game_list.html'
    context_object_name = 'game_list'
    paginate_by = 15

    def get_queryset(self):
        return Game.objects.filter(owner=self.request.user)
    

class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'board_game/publisher_detail.html'
    context_object_name = 'publisher'

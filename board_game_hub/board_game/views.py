from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Game, Publisher, GameBorrowRequest, GameRating, Discussion, Comment
from .forms import GameForm, GameRatingForm, BorrowRequestCreateForm, DiscussionForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg


def index(request):
    top_three_games = Game.objects.order_by('-rating')[:3]
    newest_games = Game.objects.order_by('-id')[:3]
    return render(request, 'board_game/index.html', {'top_three_games': top_three_games, 'newest_games': newest_games})

def game_list(request):
    game_list = Game.objects.order_by('-rating')
    paginator = Paginator(game_list, 6)
    page_number = request.GET.get('page')
    game_list = paginator.get_page(page_number)
    return render(request, 'board_game/game_list.html', {'game_list': game_list, 'page_obj': game_list})

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
    new_requests_count = GameBorrowRequest.objects.filter(request_status='New', owner=request.user).count()
    new_requests = GameBorrowRequest.objects.filter(request_status='New', owner=request.user)
    accepted_requests = GameBorrowRequest.objects.filter(owner=request.user, request_status='Accepted').order_by('-pk')[:3]
    rejected_requests = GameBorrowRequest.objects.filter(owner=request.user, request_status='Rejected').order_by('-pk')[:3]
    context = {
        'new_requests_count': new_requests_count,
        'new_requests': new_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'game_owner': request.user
    }
    return render(request, 'board_game/received_game_borrow_request_list.html', context)

@login_required
def accept_borrow_request(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    if request.user == borrow_request.owner:
        borrow_request.request_status = 'Accepted'
        borrow_request.game.status = 'Borrowed'
        borrow_request.game.save()
        borrow_request.save()
    return redirect('received_game_borrow_request_list')

@login_required
def games_others_borrowed_from_me(request):
    accepted_borrow_requests = GameBorrowRequest.objects.filter(owner=request.user, request_status='Accepted')
    borrowed_games = [borrow_request.game for borrow_request in accepted_borrow_requests if borrow_request.game.status == 'Borrowed']
    return render(request, 'board_game/games_others_borrowed.html', {'borrowed_games': borrowed_games})

@login_required
def games_i_borrowed_from_others(request):
    borrowed_games = Game.objects.filter(gameborrowrequest__borrower=request.user, gameborrowrequest__request_status='Accepted', gameborrowrequest__returned=False)
    return render(request, 'board_game/games_i_borrowed.html', {'borrowed_games': borrowed_games})

@login_required
def reject_borrow_request(request, pk):
    borrow_request = get_object_or_404(GameBorrowRequest, pk=pk)
    if request.user == borrow_request.owner:
        borrow_request.request_status = 'Rejected' 
        borrow_request.game.status = 'Available'
        borrow_request.game.save()
        borrow_request.save()
    return redirect('received_game_borrow_request_list')

@login_required
def mark_returned_confirm(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'board_game/mark_returned.html', {'game': game})

@login_required
def mark_returned(request, game_id):
    borrow_request = get_object_or_404(GameBorrowRequest, game_id=game_id)
    borrow_request.returned = True
    borrow_request.save()
    game = borrow_request.game
    game.status = 'Available'
    game.save()
    borrowed_games = Game.objects.filter(gameborrowrequest__game=game, gameborrowrequest__request_status='Accepted')
    borrowed_games.update(status='Available')
    return redirect('games_others_borrowed')


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


def discussion_list(request):
    discussions = Discussion.objects.all()
    return render(request, 'discussion/list.html', {'discussions': discussions})

def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    comments = Comment.objects.filter(discussion=discussion)
    return render(request, 'discussion/detail.html', {'discussion': discussion, 'comments': comments})

def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user
            discussion.save()
            return redirect('discussion_list')
    else:
        form = DiscussionForm()
    return render(request, 'discussion/create.html', {'form': form})

def create_comment(request, discussion_id):
    discussion = get_object_or_404(Discussion, pk=discussion_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.discussion = discussion
            comment.author = request.user
            comment.save()
            return redirect('discussion_detail', discussion_id=discussion_id)
    else:
        form = CommentForm()
    return render(request, 'discussion/create_comment.html', {'form': form, 'discussion': discussion})

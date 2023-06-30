from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('games/my/', views.UserGameListView.as_view(), name='user_game_list'),
    path('games/<int:game_id>/borrow/', views.borrow_game, name='borrow_game'),
    path('game_borrow_requests/', views.GameBorrowRequestListView.as_view(), name='game_borrow_request_list'),
    path('game_borrow_request/<int:pk>/', views.GameBorrowRequestDetailView.as_view(), name='game_borrow_request_detail'),
    path('game_borrow_request/<int:pk>/accept/', views.accept_game_borrow_request, name='accept_game_borrow_request'),
    path('game_borrow_request/<int:pk>/decline/', views.decline_game_borrow_request, name='decline_game_borrow_request'),
]

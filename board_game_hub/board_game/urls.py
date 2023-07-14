from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('game/search/', views.game_search, name='game_search'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('games/my/', views.UserGameListView.as_view(), name='user_game_list'),
    path('games/<int:game_id>/borrow/', views.create_borrow_request, name='game_borrow_request'),
    path('games/submited/', views.submited_game_borrow_list, name='submited_game_borrow_request_list'),
    path('games/received/', views.received_game_borrow_list, name='received_game_borrow_request_list'),
    path('borrow-requests/<int:pk>/accept/', views.accept_borrow_request, name='accept_borrow_request'),
    path('borrow-requests/<int:pk>/reject/', views.reject_borrow_request, name='reject_borrow_request'),
    path('games/i-borrow/', views.games_i_borrowed_from_others, name='games_i_borrowed'),
    path('games/others-borrow/', views.games_others_borrowed_from_me, name='games_others_borrowed'),
    path('game/mark_returned/<int:game_id>/', views.mark_returned, name='mark_returned'),
    path('games/create/', views.create_game, name='create_game'),
    path('games/<int:pk>/update/', views.update_game, name='update_game'),
    path('games/<int:pk>/delete/', views.delete_game, name='delete_game'),
    path('discussions/', views.discussion_list, name='discussion_list'),
    path('discussions/<int:discussion_id>/', views.discussion_detail, name='discussion_detail'),
    path('discussions/create/', views.create_discussion, name='create_discussion'),
    path('discussions/<int:discussion_id>/comment/', views.create_comment, name='create_comment'),
]

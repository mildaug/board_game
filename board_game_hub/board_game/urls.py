from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('games/my/', views.UserGameListView.as_view(), name='user_game_list'),
    path('games/<int:game_id>/borrow/', views.borrow_game, name='borrow_game'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('publisher/<int:pk>/', views.PublisherDetailView.as_view(), name='publisher_detail'),
    path('games/my/', views.UserGameListView.as_view(), name='user_game_list'),
    path('games/<int:game_id>/borrow/', views.create_borrow_request, name='game_borrow_request'),
    path('games/borrowed/', views.submited_game_borrow_list, name='submited_game_borrow_request_list'),
    path('games/received/', views.received_game_borrow_list, name='received_game_borrow_request_list'),
    path('games/create/', views.create_game, name='create_game'),
    path('games/<int:pk>/update/', views.update_game, name='update_game'),
    path('games/<int:pk>/delete/', views.delete_game, name='delete_game'),
]

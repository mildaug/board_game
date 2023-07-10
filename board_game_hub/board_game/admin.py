from django.contrib import admin
from . import models


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'language', 'difficulty', 'status')


class GameRatingAdmin(admin.ModelAdmin):
    list_display = ('game', 'rating')


class GameBorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('game', 'borrower', 'owner')


class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'author')


admin.site.register(models.Category)
admin.site.register(models.Publisher)
admin.site.register(models.Game, GameAdmin)
admin.site.register(models.GameRating, GameRatingAdmin)
admin.site.register(models.GameBorrowRequest, GameBorrowRequestAdmin)
admin.site.register(models.Discussion, DiscussionAdmin)
admin.site.register(models.Comment, CommentAdmin)

from django.contrib import admin
from . import models


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'language', 'difficulty', 'status')


class GameBorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('game', 'borrower', 'owner', 'is_accepted')


admin.site.register(models.Category)
admin.site.register(models.Publisher)
admin.site.register(models.Game, GameAdmin)
admin.site.register(models.GameBorrowRequest, GameBorrowRequestAdmin)

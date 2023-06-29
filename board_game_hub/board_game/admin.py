from django.contrib import admin
from . import models


class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'language', 'difficulty')


admin.site.register(models.Type)
admin.site.register(models.Publisher)
admin.site.register(models.Game, GameAdmin)




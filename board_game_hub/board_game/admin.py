from django.contrib import admin
from . import models


admin.site.register(models.Type)
admin.site.register(models.Publisher)
admin.site.register(models.Game)

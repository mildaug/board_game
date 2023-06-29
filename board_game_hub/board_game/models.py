from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


User = get_user_model()


class Type(models.Model):
    name = models.CharField(_('name'), max_length=100, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('type')
        verbose_name_plural = _('types')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('type_detail', kwargs={'pk': self.pk})
    

class Publisher(models.Model):
    name = models.CharField(_('name'), max_length=100, db_index=True)
    about_publisher = models.TextField(_('about_publisher'), max_length=1000)

    class Meta:
        ordering = ['name']
        verbose_name = _('publisher')
        verbose_name_plural = _('publishers')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'pk': self.pk})


class Game(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'), on_delete=models.CASCADE, related_name='games')
    title = models.CharField(_('title'), max_length=100, db_index=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_('publishers'), on_delete=models.CASCADE, related_name='games')
    type = models.ManyToManyField(Type, verbose_name=_('type(s)'))
    image = models.ImageField(_('image'), upload_to='board_game/game_images')
    player_count = models.CharField(_('player_count'), max_length=50)
    duration = models.CharField(_('duration'), max_length=50)
    player_age = models.CharField(_('player_age'), max_length=50)

    LANGUAGE_CHOICES = (
        ('EN', _('EN')),
        ('LT', _('LT')),
        ('RU', _('RU')),
        ('PL', _('PL')),
        ('Other', _('Other')),
    )

    language = models.CharField(_('languages'), max_length=50, choices=LANGUAGE_CHOICES, default='LT', db_index=True)

    DIFFICULTY_CHOICES = (
        ('Easy', _('Easy')),
        ('Medium', _('Medium')),
        ('Hard', _('Hard')),
        ('Extreme', _('Extreme')),
        ('Nightmare', _('Nightmare')),
    )

    difficulty = models.CharField(_('difficulty'), max_length=50, choices=DIFFICULTY_CHOICES, default='Medium', db_index=True)

    class Meta:
        ordering = ['title']
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})
    
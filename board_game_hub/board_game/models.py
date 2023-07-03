from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from datetime import date


User = get_user_model()


class Category(models.Model):
    name = models.CharField(_('name'), max_length=100, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk})
    

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
    owner = models.ForeignKey(User, verbose_name=_('owner'), on_delete=models.CASCADE, related_name='games', null=True, blank=True)
    title = models.CharField(_('title'), max_length=100, db_index=True)
    publisher = models.ForeignKey(Publisher, verbose_name=_('publishers'), on_delete=models.CASCADE, related_name='games')
    year = models.IntegerField(_("year"), null=True, blank=True, db_index=True)
    category = models.ManyToManyField(Category, verbose_name=_('category(-ies)'))
    rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
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

    STATUS = (
        ('Available', _('Available')),
        ('Borrowed', _('Borrowed')),
    )

    status = models.CharField(_('status'), max_length=20, choices= STATUS, blank=True, default='Available')

    class Meta:
        ordering = ['title']
        verbose_name = _('game')
        verbose_name_plural = _('games')

    def __str__(self):
        return f'{self.title}'
    
    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})
    

class GameRating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    comment = models.TextField()

    class Meta:
        ordering = ['rating']
        verbose_name = _('game rating')
        verbose_name_plural = _('game ratings')

    def __str__(self):
        return f'{self.game} {self.rating}'
    
    def get_absolute_url(self):
        return reverse('gamerating_detail', kwargs={'pk': self.pk})
    

class GameBorrowRequest(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowers')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owners')
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)
    due_back = models.DateField(_('due_back'), null=True, blank=True)

    PICK_UP_CHOICES = (
        ('Physical Exchange', _('Physical exchange')),
        ('Game Store', _('Game store')),
        ('Post', _('Post')),
        ('Pick-up Terminal', _('Pick-up terminal')),
    )

    pick_up_place = models.CharField(_('pick-up place'), max_length=20, choices=PICK_UP_CHOICES, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
    
    class Meta:
        verbose_name = _('game borrow request')
        verbose_name_plural = _('game borrow requests')

    def __str__(self):
        return f'{self.game} {self.borrower} {self.owner} {self.status}'
    
    def get_absolute_url(self):
        return reverse('gameborrowrequest_detail', kwargs={'pk': self.pk})
        
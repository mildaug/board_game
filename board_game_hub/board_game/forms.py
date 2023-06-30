from django import forms
from .models import GameBorrowRequest

class GameBorrowForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = ['message']


class GameBorrowRequestStatusForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = ['is_accepted']


class GameRatingForm(forms.Form):
    RATING_CHOICES = [
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    
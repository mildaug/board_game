from django import forms
from .models import Publisher, Category, Game, GameBorrowRequest, Discussion, Comment


class DateInput(forms.DateInput):
    input_type = 'date'


class BorrowRequestCreateForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = ['message', 'due_back']
        widgets = {
            'due_back': DateInput(),
        }


class BorrowRequestAcceptForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = []


class BorrowRequestRejectForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = []


class BorrowRequestExtendForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = ['due_back']


class BorrowRequestReturnForm(forms.ModelForm):
    class Meta:
        model = GameBorrowRequest
        fields = []


class GameRatingForm(forms.Form):
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))


class GameForm(forms.ModelForm):
    publisher = forms.ModelChoiceField(queryset=Publisher.objects.all(), required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Game
        fields = ['title', 'publisher', 'year', 'category', 'image', 'player_count', 'duration', 'player_age', 'language', 'difficulty', 'video_url']
        labels = {
            'player_count': 'Player count',
            'player_age': 'Player age', 
            'video_url': 'Link to trailer',
        }


class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']
        labels = {
            'title': 'Topic',
            'content': 'Content',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment',
        }
        
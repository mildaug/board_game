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
    
    new_publisher = forms.CharField(max_length=100, required=False)
    new_category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Game
        fields = ['title', 'publisher', 'new_publisher', 'year', 'category', 'new_category', 'image', 'player_count', 'duration', 'player_age', 'language', 'difficulty', 'video_url']

    def clean(self):
        cleaned_data = super().clean()
        publisher = cleaned_data.get('publisher')
        new_publisher = cleaned_data.get('new_publisher')
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not publisher and not new_publisher:
            raise forms.ValidationError('You must either select a publisher or enter a new one.')

        if not publisher and new_publisher:
            publisher, _ = Publisher.objects.get_or_create(name=new_publisher)
            cleaned_data['publisher'] = publisher

        if not category and new_category:
            category, _ = Category.objects.get_or_create(name=new_category)
            cleaned_data['category'] = [category]

        return cleaned_data
        

class DiscussionForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['title', 'content']
        labels = {
            'title': 'Discussion Title',
            'content': 'Discussion Content',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': 'Comment',
        }
        
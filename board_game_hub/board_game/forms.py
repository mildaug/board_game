from django import forms

class GameBorrowForm(forms.Form):
    borrower_name = forms.CharField(label='Your Name', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
    
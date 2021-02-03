from django import forms
from .models import EntryPage

class SearchForm(forms.Form):
    searched_entry = forms.CharField(max_length=120, label = '', widget=forms.TextInput(attrs={
        'placeholder': "Search entry"   }))



class EntryForm(forms.Form):
    title = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': "Entry's title"
    }))
    entry_text = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder':"Entry text"
    }))
    
    class Meta:
        model = EntryPage
        fields = [
            'title',
            'entry_text',
        ]


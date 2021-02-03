from django import forms


class SearchForm(forms.Form):
    searched_entry = forms.CharField(max_length=120, label = '', widget=forms.TextInput(attrs={
        'placeholder': "Search entry"   }))



class EntryForm(forms.Form):
    title = forms.CharField(label = '', widget = forms.TextInput(attrs={
        'placeholder': "Entry title"
    }))
    entry_text = forms.CharField(label = '', widget=forms.Textarea(attrs={
        'placeholder':"Entry text",

    }))




class EditForm(forms.Form):
    entry_text = forms.CharField(label = '', widget=forms.Textarea(attrs={
        'placeholder':"Entry text",
    }))




from typing import Callable
from .models import *
from django import forms


class AuctionForm(forms.ModelForm):

    
    class Meta:
        model = AuctionListing
        fields = [
            'title',
            'description',
            'start_bid',
            'category',
            'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs = {'class': 'form-control'}),
            'description': forms.Textarea(attrs = {'class': 'form-control', 'cols':70, 'rows':12}),
            'start_bid': forms.NumberInput(attrs = {'class': 'form-control'}),
            'category':forms.Select(attrs = {'class':"form-control"} )
            
        }
        

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets = {
             'amount': forms.NumberInput(attrs={'placeholder':"Amount (in USD$)", 'class': 'form-control' }),
            }

    def __init__(self, *args, **kwargs):
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['amount'].label = ""

        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
             'text': forms.Textarea(attrs={'class': 'form-control', 'rows':7  }),
            }
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ""
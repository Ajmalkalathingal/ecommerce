from django import forms
from .models import ProductReview
from .models import RATING

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(widget= forms.Textarea(attrs={'placeholder':'username','class':'form-control m-3'}))
    rating = forms.ChoiceField(choices=RATING, widget=forms.Select(attrs={'class': 'custom-select m-3 rounded bg-light pt-1'}))



    class Meta:
        model = ProductReview
        fields = ['review','rating']

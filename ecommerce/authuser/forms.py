from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm as DjangoPasswordResetForm
from authuser.models import User

class UserRegisterForm(UserCreationForm):
    bsform="form-control m-3 "
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username','class':bsform}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'email','class':bsform}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password','class':bsform}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':' comform password','class':bsform}))

    class Meta:
        model = User
        fields = ['username', 'email'] 


class PasswordResetForm(DjangoPasswordResetForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
        'type': 'email',
        'name': 'email',
        'id': 'email'
    }))
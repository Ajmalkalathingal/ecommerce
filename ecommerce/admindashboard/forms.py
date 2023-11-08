from django import forms
from core.models import Product,Brand,Cetogeory

class ProductForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter the title',
                'class': 'form-control m-3',
            }
        )
    )

    product_image = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control m-3',
            }
        )
    )

    selling_price = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter the selling price',
                'class': 'form-control m-3',
            }
        )
    )

    discount_rate = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Enter the discount rate',
                'class': 'form-control m-3',
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter the description',
                'class': 'form-control m-3',
            }
        )
    )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),  # Replace 'Brand' with your actual Brand model
        widget=forms.Select(
            attrs={
                'class': 'custom-select m-3 rounded bg-light pt-1',
                
            }
        )
    )

    category = forms.ModelChoiceField(
        queryset=Cetogeory.objects.all(),  # Replace 'Category' with your actual Category model
        widget=forms.Select(
            attrs={
                'class': 'custom-select m-3 rounded bg-light pt-1',
                
            }
        )
    )

    class Meta:
        model = Product
        fields = ['title','product_image','selling_price','discount_rate','description','brand','category']

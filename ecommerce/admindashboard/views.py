from django.shortcuts import render,redirect
from core.models import *
from authuser.models import *
from .forms import ProductForm

# Create your views here.

def index(request):
    user = User.objects.all().count()
    context = {
        'usercount':user
    }
    return render(request,'admindashboard/dashboard.html' ,context)


def view_user(request):
    user = User.objects.all()
    context = {
        'user':user
    }
    return render(request,'admindashboard/users.html',context)


def view_user_details(request, id):
    user = User.objects.get(id=id)
    order_product = CartOrderProduct.objects.filter(user=user)
    context = {
        'order_product' : order_product
    }
    return render(request,'admindashboard/user-details.html', context)


def list_product(request):
    qurey = request.GET.get('search')
    if qurey:
      Product_list = Product.objects.filter(title__icontains=qurey)
      return render(request, 'admindashboard/product-list.html',{'product':Product_list})
    else:
      Product_list = Product.objects.all()
      return render(request, 'admindashboard/product-list.html',{'product':Product_list})
     

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admindashboard:list-product')
    else:
        form = ProductForm()  
    return render(request, 'admindashboard/add-product.html', {'form': form})


def update_product(request, id):
    u_product = Product.objects.get(id=id)

    if request.method == "POST":
        p_form = ProductForm(request.POST, request.FILES, instance=u_product) 
        if p_form.is_valid():
            p_form.save()
            return redirect('admindashboard:list-product')
    else:
        p_form = ProductForm(instance=u_product)

    context = {
        'data': u_product,
        'p_form': p_form,
    }

    return render(request, 'admindashboard/update-product.html', context)

   


def delete_product(request,id):
    del_product = Product.objects.get(id=id)
    del_product.delete()
    return redirect('admindashboard:list-product')

from django.db.models import Avg

def review(request):
    products = Product.objects.all()
    
    product_data = []
    
    for product in products:
        product_reviews = ProductReview.objects.filter(product=product)
        average_rating = product_reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
        
        product_data.append({
            'product': product,
            'reviews': product_reviews,
            'average_rating': average_rating,
        })

    return render(request, 'admindashboard/review.html', {'product_data': product_data})

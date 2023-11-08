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

def edit_product(request, id):
    get_product = Product.objects.get(id=id)
    brand = Brand.objects.all()
    cetogeory = Cetogeory.objects.all()

    context = {
        'data':get_product,
        'brand':brand,
        'cetogeory':cetogeory,
    }
    return render(request, 'admindashboard/update-product.html', context)

def update_product(request, id):
    u_product = Product.objects.get(id=id)
    p_form = ProductForm(instance=u_product)  # Set data from the 'u_product' instance
    if request.method == "POST":
        p_form = ProductForm(request.POST, request.FILES, instance=u_product)  # Update with POST data
        if p_form.is_valid():
            print(p_form)
            p_form.save()
            return redirect('admindashboard:list-product')

    context = {
        'data': u_product,
        'p_form': p_form,
    }
    print(p_form)
    return render(request, 'admindashboard/update-product.html', context)
   


def delete_product(request,id):
    del_product = Product.objects.get(id=id)
    del_product.delete()
    return redirect('admindashboard:list-product')


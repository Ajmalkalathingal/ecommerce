from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.db.models import Max,Min

from django.http import JsonResponse,HttpResponse
from django.views import View
from django.db.models import Count,Avg
from django.shortcuts import get_object_or_404
from .forms import ProductReviewForm

from django.core import serializers
import json

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from . import views

#tag
from taggit.models import Tag

from .models import *

# def home(request):
#     product = Product.objects.filter(featured=True)

#     context = {
#          'product':product
#         }
#     return render(request, 'app/home.html',context)
     


class ProductView(View):
    def get(self, request):
        product = Product.objects.filter(featured=True)

        context = {
         'product':product
        }
        return render(request, 'app/home.html',context)
     

def product_list_view(request):
   product = Product.objects.all()

   context = {
         'product':product
        }
 
   return render(request, 'app/product_list.html', context)


def category_list_view(request):
  category = Cetogeory.objects.all()

  context = {
    'category':category
  }

  return render(request, 'app/category.html', context)


def category_product_list(request,cid):
  category = Cetogeory.objects.get(cid=cid)
  product = Product.objects.filter(category=category)

  context = {
    'category': category,
    'product' : product,
  }

  return render(request, 'app/category_list_view.html', context)


def product_datail_view(request, id):
  
  product = Product.objects.get(id=id)
  # product = get_object_or_404(Product,id=id)

  # related product
  products = Product.objects.filter(category= product.category).exclude(id=id)[:10]

  # review
  review = ProductReview.objects.filter(product=product).order_by('-date')

  # review rating
  average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

  # review form
  review_form = ProductReviewForm()

  # make review
  make_review = True
  if request.user.is_authenticated:
      user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
  
      if user_review_count > 0:
        make_review = False


  

  context = {
    'p':product,
    'products': products,
    'review': review,
    'rating': average_rating,
    'review_form': review_form,
    'make_review': make_review
  }
  return render(request,'app/productdetail.html',context)


def tag_view(request, slug):
  product = Product.objects.all().order_by('-id')

  # tag = None
   
  tag = get_object_or_404(Tag, slug=slug) #slug is Tag model attribute
  products = product.filter(tag__in=[tag])

  context = {
    'product' : products,
    'tag' : tag,
  }

  return render(request,'app/tag.html', context)



def add_ratting(request, id):
  product = Product.objects.get(id=id)
  user = request.user

  review = ProductReview.objects.create(
    user=user,
    product=product,
    review = request.POST['review'],
    rating = request.POST['rating']
  )

  context = {
    'user': user.username,
    'review' : request.POST['review'],
    'rating' : request.POST['rating'],
  }


  average_review = ProductReview.objects.filter(product=product).aggregate(rating = Avg('rating'))

  return JsonResponse(
    {
      'bool' : True,
      'context' : context,
      'average_review' : average_review
    }
  )


def search_product(request):

  qurey = request.GET.get('q')

  product = Product.objects.filter(title__icontains=qurey)

  context = {
    'query' : qurey,
    'product' : product
  }

  return render(request,'app/search.html', context)


def store(request):

  cetogory = Cetogeory.objects.all()

  brand = Brand.objects.all()

  product = Product.objects.all()

  # filter by price
  max_min_price = Product.objects.aggregate(Max('selling_price'), Min('selling_price'))

  context = {
    'cetogory': cetogory,
    'brand' : brand,
    'product': product,
    'max_min_price' : max_min_price,
  }

  return render(request, 'app/store.html', context)


# filter product
def filter_product(request):
  cetogory = request.GET.getlist('cetogory[]')
  brand = request.GET.getlist('brand[]')

  # filter by price
  max_price = request.GET['max_price']
  min_price = request.GET['min_price']
  
  product = Product.objects.all()

  
  print(max_price,min_price)

  product = product.filter(selling_price__gte = min_price)
  product = product.filter(selling_price__lte = max_price)


  if len(cetogory) > 0:
    product = product.filter(category__id__in = cetogory).order_by('-id').distinct()

  if len(brand) > 0:
    product = product.filter(brand__id__in = brand).distinct()

  data = render_to_string('app/async/productlist.html', {'product':product})
  return JsonResponse({'data':data})

# ===================================================================================================================#


# add to cart

def add_to_cart(request):
    user = request.user
    product_id = float(request.GET['id'])
    quantity = int(request.GET['qty'])

    product = get_object_or_404(Product, id=product_id)

    #  to get the cart item if it exists
    cart_item = CartItem.objects.filter(user=user, product=product, id=product.id).first()

    if cart_item:
        cart_item.quantity = quantity
        cart_item.save()

    else:
        cart_item = CartItem.objects.create(user=user, product=product, quantity=quantity, id=product.id)

    return JsonResponse({
        'data': {
            'id': cart_item.product.id,
            'title': cart_item.product.title,
            'price': product.discount_rate,
            'quantity': cart_item.quantity,
            'image': cart_item.product.product_image.url,
        },
    })




def cart(request):
    cart_items = CartItem.objects.filter(user=request.user).order_by('-id')
    cart_total = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }

    return render(request, 'app/cart.html', context)


@login_required
def remove_from_cart(request):
    product_id = request.GET.get('id')
    print(product_id)

    if product_id is not None:
        # Ensure product_id is an integer
        product_id = int(product_id)
        
        try:
            cart_item = CartItem.objects.get(user=request.user, id=product_id)
            print(cart_item)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.total_price() for item in cart_items)

    context = render_to_string('app/async/remove-cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

    return JsonResponse({'data': context, 'success': True})


@login_required
def refresh_from_cart(request):
    product_id = request.GET.get('product_id')
    product_qty = request.GET.get('product_qty')

    print(product_id)
    print(product_qty)

    if product_id is not None:
        try:
            product_id = int(product_id)
            product_qty = int(product_qty)

            cart_item = CartItem.objects.get(user=request.user, id=product_id)
            cart_item.quantity = product_qty
            cart_item.save()

        except (CartItem.DoesNotExist, ValueError):
            pass

    cart_items = CartItem.objects.filter(user=request.user)
    cart_total = sum(item.total_price() for item in cart_items)

    context = render_to_string('app/async/remove-cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

    return JsonResponse({'data': context, 'success': True})  


@login_required
def check_out_page(request):
    # Retrieve the cart items for the user
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = 0
    cart_total_amount = 0  # Initialize the cart_total_amount

    # Calculate the total amount for the cart item
    for item in cart_items:
        cart_total_amount+= item.total_price()
        

    # Calculate the total amount for the PayPal payment and create a CartOrder
    order = CartOrder.objects.create(user=request.user, price=cart_total_amount)
    for item in cart_items:
        total = item.total_price()
        total_amount += total

        # Create a CartOrderProduct entry for each cart item
        cart_order_product = CartOrderProduct.objects.create(user=request.user,
            order=order,
            item=item.product.title,
            image=item.product.product_image.url,
            qty=item.quantity,
            price=item.product.discount_rate,
            total=total
        )

    host = request.get_host()
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total_amount,
        "item_name": "order-item no",
        "invoice": "No 5",
        "currency": "USD",
        "notify_url": "http://{}{}".format(host, reverse("app:paypal-ipn")),
        "return_url": "http://{}{}".format(host, reverse("app:payment-complete")),
        "cancel_url": "http://{}{}".format(host, reverse("app:payment-cancel")),
    }

    paypal_payment_btn = PayPalPaymentsForm(initial=paypal_dict)
    # print(paypal_payment_btn)

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
      total = item.total_price()
      total_amount += total
      return render(request, 'app/checkout.html', {'cart_items': cart_items, 'cart_total': cart_total_amount, 'paypal_payment': paypal_payment_btn})


    # Clear the cart items for the user after processing the order

    return render(request, 'app/checkout.html')


def payment_complete(request):
      cart_items = CartItem.objects.filter(user=request.user)
      cart_total = sum(item.total_price() for item in cart_items) 

      return render(request,'app/paymentcompleted.html', {'cart_items': cart_items, 'cart_total': cart_total})  


def payment_cancel(request):
  return render(request,'app/paymentcancel.html')


@login_required
def customer_dash_bord(request):
   return render(request, 'app/customerdashbord.html') 

login_required
def customer_order(request):
   order= CartOrderProduct.objects.all()
   return render(request,'app/order.html',{'data':order})


@login_required
def order_details(request, id):
    # Use get_object_or_404 to retrieve the order or return a 404 page if it doesn't exist
    order = get_object_or_404(CartOrder, id=id)
    # Ensure the user can only access their own orders
    if request.user != order.user:
        return HttpResponse("You don't have permission to view this order.")
    orders = CartOrderProduct.objects.filter(order=order)

    context = {
        'orders': orders
    }

    return render(request, 'app/orderdetails.html', context)

           






# @login_required
# def customer_order(request):
#     # Fetch orders for the logged-in user
#     order = CartOrder.objects.filter(user=request.user).first()  # Use .first() to get a single result
#     if order:
#         orders = CartOrderProduct.objects.filter(user=request.user, order=order)
#         orders_data = serializers.serialize('json',orders)
#         order_info = {
#             'order': orders_data
#         }
#         return JsonResponse(order_info)
#     else:
#         return JsonResponse({'error': 'No orders found for this user'})




def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')







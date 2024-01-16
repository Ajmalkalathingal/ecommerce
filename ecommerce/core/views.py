from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.db.models import Max,Min

from django.http import JsonResponse,HttpResponse
from django.views import View
from django.db.models import Count,Avg
from django.shortcuts import get_object_or_404
from .forms import ProductReviewForm

# from django.core import serializers
# import json

from django.urls import reverse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from . import views

#tag
from taggit.models import Tag

from .models import *

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

def brand_product_list(request,id):
  brand = Brand.objects.get(id=id)
  product = Product.objects.filter(brand=brand)

  context = {
    'brand': brand,
    'product' : product,
  }

  return render(request, 'app/brand-list.html', context)


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def product_datail_view(request, id):
    product = Product.objects.get(id=id)

    # related product
    products = Product.objects.filter(category=product.category).exclude(id=id)[:10]

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

    # pagination
    reviews_per_page = 3
    paginator = Paginator(review, reviews_per_page)
    page = request.GET.get('page')

    try:
        reviews_page = paginator.page(page)
    except PageNotAnInteger:
        reviews_page = paginator.page(1)
    except EmptyPage:
        reviews_page = paginator.page(paginator.num_pages)

    context = {
        'p': product,
        'products': products,
        'reviews_page': reviews_page,
        'rating': average_rating,
        'review_form': review_form,
        'make_review': make_review,
    }

    return render(request, 'app/productdetail.html', context)


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


@login_required
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

  if qurey:
    product = Product.objects.filter(title__icontains=qurey)
    context = {
      'query' : qurey,
      'product' : product
    }
    return render(request,'app/search.html', context)
  
  return render(request, 'app/home.html')


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


# add to cart and wish list

@login_required
def add_to_wish_list(request):
    product_id = request.GET.get('id')
    product = get_object_or_404(Product, id=product_id)

    wish_list, created = WishList.objects.get_or_create(user=request.user, product=product)

    if created:
        wish_list_count = WishList.objects.filter(user=request.user).count()
        return JsonResponse({'data': {
            'id': wish_list.product.id,
            'title': wish_list.product.title,
            'price': product.discount_rate,
            'image': wish_list.product.product_image.url,
            'wish_list_count' : wish_list_count

        }})
    else:
        return JsonResponse({'error': 'Product already in wish list'})

@login_required
def wish_list(request):
    
    wish_list_items = WishList.objects.filter(user=request.user).order_by('-id')
    wish_list_count = WishList.objects.filter(user=request.user).count()
    
    context = {
        'wish_list_items': wish_list_items,
        'wish_list_count' : wish_list_count
    }
    
    return render(request, 'app/wish_list.html', context)

@login_required
def delete_wish_list(request, id):
    product = get_object_or_404(Product, id=id)
    delete_wish = WishList.objects.filter(user=request.user, product=product)
    delete_wish.delete()

    return redirect('app:wish-list')

@login_required
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

    cart_count = CartItem.objects.filter(user=user).count()


    return JsonResponse({
        'data': {
            'id': cart_item.product.id,
            'title': cart_item.product.title,
            'price': cart_item.product.discount_rate,
            'quantity': cart_item.quantity,
            'image': cart_item.product.product_image.url,
            'cart_count': cart_count,            
            
        },
    })


@login_required
def cart(request):
    user = request.user
    cart_count = CartItem.objects.filter(user=user).count()
    cart_items = CartItem.objects.filter(user=request.user).order_by('-id')
    cart_total = sum(item.total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_count': cart_count,
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
def check_out_page(request, id=None):
    cart_total_amount = 0
    address = []

    cart_items = CartItem.objects.filter(user=request.user)
  
    # Calculate the total amount for the cart item
    for item in cart_items:
      cart_total_amount+= item.total_price()
          
    try:
      address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
      pass  

    context = {
      'cart_items': cart_items,
      'cart_total': cart_total_amount, 
      'address': address
    }

    return render(request, 'app/checkout.html',context)


@login_required
def process_payment(request):
    if request.method == 'POST':
      user = request.user
      payment_mode = request.POST.get('payment_mode')

      cart_items = CartItem.objects.filter(user=user)
      total_amount = 0
      default_address = Address.objects.filter(user=user, status=True).first()

      # Create a CartOrder for the user's purchase

      for item in cart_items:
          total_amount += item.total_price()
          
          # Create a CartOrderProduct entry for each item in the cart
          order = CartOrder.objects.create(user=user, price=total_amount, address=default_address, payment_mode=payment_mode)
          cart_order_product = CartOrderProduct.objects.create(
              user=user,
              id=order.id,
              order=order,
              item=item.product.title,
              image=item.product.product_image.url,
              qty=item.quantity,
              price=item.product.discount_rate,
              total=item.total_price()
          )
      if payment_mode == 'paid by Razor pay':
         return JsonResponse({'status': 'payment is successfully'})
      
      # After checkout, delete cart items
      # cart_items.delete()

    return redirect('app:home')


def razorpay_total(request):
   cart = CartItem.objects.filter(user=request.user)
   total_amount = 0

   for item in cart:
      total_amount += item.total_price()

   return JsonResponse({'tatal_amount': total_amount})  


def order(request):
      order= CartOrderProduct.objects.filter(user = request.user)
      return render(request,'app/order.html', {'order_items': order,})  


def payment_cancel(request):
  return render(request,'app/paymentcancel.html')


@login_required
def customer_dash_bord(request):
  order= CartOrderProduct.objects.filter(user = request.user)
  customer_address = Address.objects.filter(user= request.user)

  if request.method == 'POST':

    name = request.POST.get('name')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    city = request.POST.get('city')
    zipcode = request.POST.get('zipcode')
    state = request.POST.get('state')
    new_address = Address.objects.create(
        user = request.user,
        name = name,
        address = address,
        phone = phone,
        city = city,
        zipcode = zipcode,
        state = state
      )

    return redirect('app:dashbord')

  context = {
    'order' : order,
    'address' : customer_address
   }
  return render(request, 'app/customerdashbord.html', context) 


def make_dafault_address(request):
   id = request.GET.get('id')
   Address.objects.update(status = False)
   Address.objects.filter(id = id).update(status = True)

   return JsonResponse({
      'boolean' : True
   })


@login_required
def order_details(request, id):
    # Use get_object_or_404 to retrieve the order or return a 404 page if it doesn't exist
    order = get_object_or_404(CartOrder, id=id)

    # Ensure the user can only access their own orders
    if request.user != order.user:
        return HttpResponse("You don't have permission to view this order.")

    address = order.address 

    orders = CartOrderProduct.objects.filter(order=order)

    context = {
        'orders': orders,
        'address': address,
    }

    return render(request, 'app/orderdetails.html', context)


@login_required
def check_out_page(request, id=None):
    cart_total_amount = 0
    address = []

    cart_items = CartItem.objects.filter(user=request.user)
  
    # Calculate the total amount for the cart item
    for item in cart_items:
      cart_total_amount+= item.total_price()
          
    try:
      address = Address.objects.get(user=request.user, status=True)
    except Address.DoesNotExist:
      pass  

    context = {
      'cart_items': cart_items,
      'cart_total': cart_total_amount, 
      'address': address
    }

    return render(request, 'app/checkout.html',context)



# @login_required
# def check_out_page(request, id=None):
#     total_amount = 0
#     cart_total_amount = 0
#     cart_items = [] 
#     product = [] 
#     address = []

#     # Check if an ID is provided (Buy Now button) or not (cart items)
#     default_address= Address.objects.filter(user=request.user, status=True).first()
#     if id is not None:
#         # Get the product by ID
#         product = Product.objects.get(id=id)

#         # Check if the user is authenticated
#         if request.user.is_authenticated:
#             # Create a CartOrder for the user
#             order = CartOrder.objects.create(user=request.user, price=product.discount_rate, address=default_address)

#             # Create a CartOrderProduct entry for the product
#             cart_order_product = CartOrderProduct.objects.create(
#                 user=request.user,
#                 order=order,
#                 id = order.id,
#                 item=product.title,
#                 image=product.product_image.url,
#                 qty=product.qty, 
#                 price=product.discount_rate,
#                 total=product.discount_rate
#             )
#             cart_total_amount=product.discount_rate
#             total_amount=product.discount_rate
#     else:  

#         cart_items = CartItem.objects.filter(user=request.user)
     
#         # Calculate the total amount for the PayPal payment and create a CartOrder
#         for item in cart_items:
#             total = item.total_price()
#             total_amount += total
      
#         # Calculate the total amount for the cart item
#         for item in cart_items:
#             cart_total_amount+= item.total_price()
#             # Create a CartOrderProduct entry for each cart item
#             order = CartOrder.objects.create(user=request.user, price=cart_total_amount, address= default_address)
#             cart_order_product = CartOrderProduct.objects.create(user=request.user,
#                     order=order,
#                     id = order.id,
#                     item=item.product.title,
#                     image=item.product.product_image.url,
#                     qty=item.quantity,
#                     price=item.product.discount_rate,
#                     total=total
#                 )
#     print(total_amount)
#     print(cart_total_amount)   

#     host = request.get_host()

#     # Create a PayPal payment form
#     paypal_dict = {
#         "business": settings.PAYPAL_RECEIVER_EMAIL,
#         "amount": total_amount,
#         "item_name": "Order Item No",
#         "invoice": "No 5",
#         "currency": "USD",
#         "notify_url": "http://{}{}".format(host, reverse("app:paypal-ipn")),
#         "return_url": "http://{}{}".format(host, reverse("app:payment-complete")),
#         "cancel_url": "http://{}{}".format(host, reverse("app:payment-cancel")),
#     }
    
#     # checking user make address
#     try:
#       address = Address.objects.get(user=request.user, status=True)
#     except Address.DoesNotExist:
#       pass  

#     paypal_payment_btn = PayPalPaymentsForm(initial=paypal_dict)

#     # Clear the cart items for the user after processing the order
#     # cart_items.delete()

#     context = {
#       'cart_items': cart_items,
#       'cart_total': cart_total_amount, 
#       'paypal_payment': paypal_payment_btn,
#       'product': product,
#       'address': address
#     }

#     return render(request, 'app/checkout.html',context)
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'app'

urlpatterns = [

    # path('', views.home, name='home'),
    path('',views.ProductView.as_view(),name='home'),
    path('product/', views.product_list_view, name='product_list'),
    path('category/', views.category_list_view, name='category'),
    path('category/<cid>/', views.category_product_list, name='category_product_list'),
    path('brand/<id>/', views.brand_product_list, name='brand_product_list'),

    # prodcut details
    path('product-details/<id>/',views.product_datail_view, name='productdetail'),

    # tags
    path('product/tag/<slug:slug>/', views.tag_view, name='tag'),

    # adding review
    path('review/<int:id>', views.add_ratting, name='review'),

    # search
    path('search', views.search_product, name='search'),

    # filter product
    path('store', views.store, name='store'),
    path('filter-products/', views.filter_product, name='filter-product'),

    # add to cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.cart, name='cart'),

    #remove from cart
    path('remove-from-cart/', views.remove_from_cart, name='remove-from-cart'),

    # refresh from cart
    path('refresh-from-cart/', views.refresh_from_cart, name='refresh-from-cart'),
    
    # add to wish list
    path('add-to-wish-list/', views.add_to_wish_list, name='add-to-wish-list'),
    path('wish-list/', views.wish_list, name='wish-list'),
    path('delete-wish-list/<int:id>', views.delete_wish_list, name='delete-wish-list'),


    # checkout page
    path('checkout/', views.check_out_page, name='checkout'),
    path('checkout/<int:id>/', views.check_out_page, name='checkout_with_product'),

    # payment
    path('process-payment', views.process_payment, name='process-payment'),
    path('payment-proceed/', views.razorpay_total, name='payment-proceed'),



    path('paypal/', include("paypal.standard.ipn.urls"),name='paypal-ipn'),
    path('payment-complete/', views.order, name='payment-complete'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
    

    # dash bord
    path('dashbord/', views.customer_dash_bord, name='dashbord'),
    path('orders/<int:id>', views.order_details, name='orders-details'),
    
    # make_dafault_address
    path('make-default-address/',views.make_dafault_address, name='make-default-address'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

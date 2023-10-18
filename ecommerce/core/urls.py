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

    # checkout page
    path('checkout/', views.check_out_page, name='checkout'),


    # payment
    path('paypal/', include("paypal.standard.ipn.urls"),name='paypal-ipn'),
    path('complete/', views.payment_complete, name='payment-complete'),
    path('cancel/', views.payment_cancel, name='payment-cancel'),
    

    # dash bord
    path('dashbord/', views.customer_dash_bord, name='dashbord'),
    path('orders/', views.customer_order, name='orders'),
    path('orders/<int:id>', views.order_details, name='orders-details'),








    










    # path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('mobile/', views.mobile, name='mobile'),
    path('registration/', views.customerregistration, name='customerregistration'),

    # path('', views.home, name='home'),
    # # path('',views.ProductView.as_view(),name='home'),
    # path('product/', views.product_list_view, name='product_list'),
    # path('category/', views.category_list_view, name='category'),
    # path('category/<cid>/', views.category_product_list, name='category_product_list'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

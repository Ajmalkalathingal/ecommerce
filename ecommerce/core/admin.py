from django.contrib import admin
from .models import(Customer, Product, CartOrder,Brand,Cetogeory,ProductReview,CartItem,CartOrderProduct)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality','city','zipcode', 'state']

@admin.register(Product)
class ProductModleAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discount_rate', 'description', 'brand', 'featured', 'category', 'product_image' ] 

@admin.register(CartOrder)
class CartAdminModel(admin.ModelAdmin):
    list_editable = ['paid_status', 'status']
    list_display = ['user', 'price', 'paid_status','orderd_date','status']  

@admin.register(CartOrderProduct)
class OrderplacedAdminModel(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'qty',]

@admin.register(Cetogeory)
class CetogeryAdminModel(admin.ModelAdmin):
    list_display = ['id','title',] 

@admin.register(ProductReview)
class ProductReviewAdminModel(admin.ModelAdmin):
    list_display = ['user','review','product','rating']

@admin.register(Brand)
class BrandviewAdminModel(admin.ModelAdmin):
    list_display = ['brand_name','image','id']  
           

admin.site.register(CartItem)           
           

from django.db import models
from authuser.models import User
# from django.utils import timezone
import uuid
from taggit.managers import TaggableManager



class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product', null=True)

    def __str__(self):
        return self.brand_name
    

class Cetogeory(models.Model):
    cid = models.CharField(
        max_length=22,
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.BooleanField(default=False,)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='product')
    selling_price = models.DecimalField(max_digits=999999999, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=999999999, decimal_places=2)
    description = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Cetogeory, on_delete=models.SET_NULL, null=True, related_name='category')
    qty = models.IntegerField(default=1, null=True)
    


    tag = TaggableManager(blank=True)
  
    featured = models.BooleanField(default=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_percentage(self):
        new_price = (self.discount_rate / self.selling_price) * 100
        return new_price
    


STATUS_CHOICE = (
    ('accepted','accepted'),
    ('process','process'),
    ('shipped','shipped'),
    ('delivered','delivered'),  
    ('cancel','cancel'),
)

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)


    price = models.DecimalField(max_digits=9999999, decimal_places=2)
    payment_mode = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True) 
    paid_status = models.BooleanField(default=False)
    orderd_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default='pending') 


class CartOrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True) 
    invoice_no = models.CharField(max_length=100,null=True)
    item = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=100, null=True)
    qty = models.IntegerField(default=0, null=True)
    price = models.DecimalField(max_digits=99999999, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=999999, decimal_places=2, null=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, null=True)
    quantity = models.PositiveIntegerField(default=0)
    image = models.URLField(null=True)

    def total_price(self):
        return self.product.discount_rate * self.quantity
    

# rating product
RATING = (
    (1,'⭐☆☆☆☆'),
    (2,'⭐⭐☆☆☆'),
    (3,'⭐⭐⭐☆☆'),
    (4,'⭐⭐⭐⭐☆'),
    (5,'⭐⭐⭐⭐⭐')
)

class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def average_rating(self, obj):
        reviews = ProductReview.objects.filter(product=obj)
        if reviews.exists():
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / reviews.count()
        return 0
 

class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True, null=True)
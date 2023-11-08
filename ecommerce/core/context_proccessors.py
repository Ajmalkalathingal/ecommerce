# context for the base. categoriey dropdown menu verann 
# insatll in setting .py TEMPLATES section list as
# 'core.context_proccesser.defualt'

from .models import *


def default(request):
    categories = Cetogeory.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()


    cart_count = 0
    wish_list_count = 0
    if request.user.is_authenticated:
        try:
            cart_count = CartItem.objects.filter(user=request.user).count()
        except CartItem.DoesNotExist:
            pass

        try:
            wish_list_count = WishList.objects.filter(user=request.user).count()
        except WishList.DoesNotExist:
            pass
        
    return {
        'categories': categories,
        'product': product,
        'brand': brand,
        'cart_count' :cart_count,
        'wish_list_count': wish_list_count
    }
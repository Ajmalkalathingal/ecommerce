# context for the base. categoriey dropdown menu verann 
# insatll in setting .py TEMPLATES section list as
# 'core.context_proccesser.defualt'

from .models import *


def default(request):
    categories = Cetogeory.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    return {
        'categories': categories,
        'product': product,
        'brand': brand,
    }
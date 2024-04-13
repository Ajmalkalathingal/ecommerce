django taggit -> used to tags like #fashin #cosmetics
first pip install django-taggit
second add setting.py -> installed app -> taggit
third -> models.py import-> from taggit.manager import TaggableManager 


payment 
pip insatll django-paypal
setting.py -> insatlled app ->paypal.standerd.ipn
urls.py -> path('paypal',include('paypal-standard.ipn.urls))
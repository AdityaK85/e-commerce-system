from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(contactUs)
admin.site.register(category)
admin.site.register(user_login)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(user_order)
admin.site.register(order_item)
admin.site.register(profile)
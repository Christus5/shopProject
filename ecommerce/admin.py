from django.contrib import admin

from ecommerce.models import *

admin.site.register([Item, Tag, Order, Info, ItemImage, Cart])

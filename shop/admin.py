from django.contrib import admin
from .models import Product
from .models import Order, OrderItem #Cho admin quản lý đơn

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
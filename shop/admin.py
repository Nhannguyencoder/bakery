from django.contrib import admin
from .models import Product
from .models import Order, OrderItem #Cho admin quản lý đơn
from .models import Category #Phân loại sản phẩm

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'created_at')
    inlines = [OrderItemInline]
    list_filter = ('status',)
    search_fields = ('name', 'phone')

admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Category)
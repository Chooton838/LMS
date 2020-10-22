from django.contrib import admin
from .models import Product, Order, OrderItem, Customer


admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)



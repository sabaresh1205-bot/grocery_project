from django.contrib import admin
from .models import Products, Partners, Customers, Orders, OrderItems

admin.site.register(Products)
admin.site.register(Partners)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(OrderItems)
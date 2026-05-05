from django.contrib import admin
from .models import Products, Partners, Customers, Orders, OrderItems

admin.site.register(Products)
admin.site.register(Partners)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(OrderItems)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_cover_image')

admin.site.register(Products, ProductAdmin)
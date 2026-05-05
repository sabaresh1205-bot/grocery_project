from django.contrib import admin
from .models import Products, Partners, Customers, Orders, OrderItems
from django.utils.html import format_html


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'image_preview')

    def image_preview(self, obj):
        if obj.product_cover_image:
            return format_html('<img src="{}" width="100" />', obj.product_cover_image)
        return "No Image"

    image_preview.short_description = "Image"

admin.site.register(Products, ProductAdmin)
admin.site.register(Partners)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(OrderItems)
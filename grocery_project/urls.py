from django.contrib import admin
from django.urls import path
from products.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', home , name='home'),
    path('Groceryshop/Products/', products, name="products"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('View-Cart/', viewCart, name='viewCart'),
    path('remove_from_cart/<str:key>', RemoveFromCart, name="RemoveFromCart"),
    path('increase_qty/<str:key>/', increaseQty, name="increaseQty"),
    path('decrease_qty/<str:key>/', decreaseQty, name='decreaseQty'),
    path('checkout/', PlaceOrder, name='checkOut'),
    path('order_review/<int:order_id>/', order_review, name='order_review'),
    path('create_payment/<str:order_id>/',create_payment, name='create_payment'),
    path('payment_success/',payment_success, name="payment_success"),
    path('success_page/', success_page, name="success_page"),
    path('Pending_Orders/', pending_orders, name='pending_orders'),
    path('completed-orders/', completed_orders, name='completed_orders'),
    path('Order-Details/<int:orderId>/', order_details, name='order_details'),
    path('customerRegister/', customerRegister, name="customerRegister"),
    path('customerLogin/', customerLogin, name="customerLogin"),
    path('customerDashboard/', customerDashboard, name="customerDashboard"),
    path('partnerRegister/', partnerRegister, name="partnerRegister"),
    path('partnerLogin/', partnerLogin, name="partnerLogin"),
    path('partnerDashboard/', partnerDashboard, name="partnerDashboard"),
    path('addproducts/', addProducts, name="addProducts"),
    path('product_list/',productList, name="productList"),
    path('delete/<int:product_id>/', deleteProduct, name='deleteProduct'),
    path('edit/<int:product_id>/', editProduct, name='editProduct'),
    path('contact/',contact, name="contact"),
    path('admin/', admin.site.urls),
]



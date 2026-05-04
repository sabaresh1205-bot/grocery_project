from django.db import models

class Partners(models.Model):
    partner_id = models.AutoField(primary_key=True)
    partner_created = models.CharField(max_length=255)
    partner_name = models.CharField(max_length=255)
    partner_email = models.CharField(max_length=255)
    partner_mobile = models.CharField(max_length=255)
    partner_password = models.CharField(max_length=255)
    partner_address = models.CharField(max_length=255)
    partner_state = models.CharField(max_length=255)
    partner_city = models.CharField(max_length=255)
    partner_pincode = models.BigIntegerField()
    partner_status = models.CharField(max_length=255)

    class Meta:
        db_table= "ecomm_partners"

    def __str__(self):
        return self.partner_name
    
class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_mobile = models.CharField(max_length=255)
    customer_password = models.CharField(max_length=255)

    class Meta:
        db_table = "ecomm_customers"
    def __str__(self):
        return self.customer_name
    
class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_by = models.BigIntegerField()
    product_created = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.FloatField()
    product_quantity = models.IntegerField()
    product_cover_image = models.ImageField(blank=True, null=True)
    product_status = models.CharField(max_length=255)

    class Meta:
        db_table = "ecomm_products"

    def __str__(self):
        return self.product_name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    order_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.BigIntegerField()
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    payment_method = models.CharField(max_length=255)
    razorpay_order_id = models.CharField(max_length=100, blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    payment_status = models.CharField(max_length=255)
    order_status = models.CharField(max_length=255)
    created_at = models.CharField(max_length=255)

    class Meta:
        db_table = "orders"

    def __str__(self):
        return self.order_number
    
class OrderItems(models.Model):
    item_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField()
    item_pro_id = models.IntegerField()
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "order_items"

    def __str__(self):
        return self.item_name

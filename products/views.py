import razorpay 
import json
import random
import time
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Partners
from .models import Customers
from .models import Products, Orders, OrderItems
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from razorpay.errors import SignatureVerificationError
import cloudinary.uploader

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

def home(request):
    return render(request, 'index.html')

def products(request):
    allProducts= Products.objects.all()
    cart = request.session.get('cart', {})
    cart_count= sum(item['qty'] for item in cart.values())
    return render(request, 'products.html',{'products':allProducts,'cart_count': cart_count})

def customerRegister(request):
    if request.method == "POST":
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_mobile = request.POST.get('customer_mobile')
        customer_password = request.POST.get('customer_password')

        if not customer_password:
            return render(request, "customer_Register.html",{
                'error': 'Password is required'
            })
        
        if Customers.objects.filter(customer_email=customer_email).exists():
            return render(request, "customer_Register.html", {
                'error': 'Password is required'
            })
        
        Customers.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_mobile=customer_mobile,
            customer_password=make_password(customer_password)
        )
    return render(request, 'customer_Register.html')

def customerLogin(request):
    if request.method == "POST":
        email=request.POST.get('customer_email')
        password=request.POST.get('customer_password')

        try:
            users= Customers.objects.get(customer_email=email)

            if check_password(password, users.customer_password):
                request.session['id'] = users.customer_id
                request.session['customer_name']= users.customer_name
                return redirect('customerDashboard')
            else:
                return render(request, "customer_Login.html",{
                    'error': "Invalod email or password"
                })
            
        except Customers.DoesNotExist:
            return render(request, "customer_Login.html",{
                'error': "Customer not found"
            })


    return render(request, 'customer_Login.html')

def customerDashboard(request):
    if not request.session.get('id'):
        return redirect('customerLogin')
    
    return render(request, "customer_Dashboard.html",{
        'customer_name': request.session.get('customer_name')
    })

def partnerRegister(request):
    if request.method == "POST":
        partner_created = request.POST.get('partner_created')
        partner_name = request.POST.get('partner_name')
        partner_email = request.POST.get('partner_email')
        partner_mobile = request.POST.get('partner_mobile')
        partner_password = request.POST.get('partner_password')
        partner_address = request.POST.get('partner_address')
        partner_state = request.POST.get('partner_state')
        partner_city = request.POST.get('partner_city')
        partner_pincode = request.POST.get('partner_pincode')
        partner_status = request.POST.get('partner_status')

        if Partners.objects.filter(partner_email=partner_email).exists():
            return render(request, "partner/partner_Register.html",{
                'error': 'User already Registered'
            })
        
        Partners.objects.create(
             partner_created=partner_created,
             partner_name=partner_name,
             partner_email=partner_email,
             partner_mobile=partner_mobile,
             partner_password=make_password(partner_password),
             partner_address=partner_address,
             partner_state=partner_state,
             partner_city=partner_city,
             partner_pincode=partner_pincode,
             partner_status=partner_status
        )

        return render(request, "partners/partner_Register.html",{
            'success':'partner resigtered successfully'
        })
    return render(request, "partners/partner_Register.html")

def partnerLogin(request):
    if request.method == "POST":
        email = request.POST.get('partner_email')
        passwoed = request.POST.get('partner_password')

        try:
            user = Partners.objects.get(partner_email=email)

            if check_password(passwoed, user.partner_password):
                request.session['id'] = user.partner_id
                request.session['partner_name'] = user.partner_name
                return redirect('partnerDashboard')
            else:
                return render(request, "partners/partner_Login.html", {
                    'error': "Invalid email or password"
                })

        except Partners.DoesNotExist:
            return render(request, "partners/partner_Login.html", {
                'error': "Partner not found"
            })

    return render(request, 'partners/partner_Login.html')

def partnerDashboard(request):
    if not request.session.get('id'):
        return redirect('partners/partnerLogin')
    
    return render(request, "partners/partner_Dashboard.html",{
        'partner_name': request.session.get('partner_name')
    })

import cloudinary.uploader

def addProducts(request):
    if request.method == "POST":
        image = request.FILES.get('product_cover_image')

        print("IMAGE:", image)  # check file coming

        if image:
            result = cloudinary.uploader.upload(image)
            print("UPLOAD RESULT:", result)  # 🔥 VERY IMPORTANT

            return HttpResponse(result['secure_url'])  # TEMP TEST

    return render(request, 'partners/add_Products.html')

def productList(request):
    Myproducts = Products.objects.filter(product_by=request.session.get('id'))
    return render(request, 'partners/product_List.html',{'products':Myproducts})

def add_to_cart(request, product_id):
    cart= request.session.get('cart', {})
    CartProduct =get_object_or_404(Products, product_id=product_id)
    product_id=str(product_id)

    if product_id in cart:
        cart[product_id]['qty'] += 1
    else:
        cart[product_id] = {
            'ProductName': CartProduct.product_name,
            'ProductPrice': float(CartProduct.product_price),
            'qty': 1,
            'proimg': CartProduct.product_cover_image.url
        }

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('products')

def viewCart(request):
    cart = request.session.get('cart', {})

    total = 0
    cart_count = 0

    for item in cart.values():
        item['subtotal'] = item['ProductPrice'] * item['qty']
        total += item['subtotal']
        cart_count += item['qty']
    request.session['cart'] = cart

    return render(request, 'view_cart.html', {
        'cart': cart,
        'total': total,
        'cart_count': cart_count
    })

def RemoveFromCart(request, key):
    cart = request.session.get('cart', {})

    if key in cart:
        del cart[key]
        request.session['cart'] = cart
    return redirect('viewCart')

def increaseQty(request, key):
    cart = request.session.get('cart', {}) 
    if key in cart:
        cart[key]['qty'] += 1
    request.session['cart'] = cart 
    return redirect('viewCart')

def decreaseQty(request, key):
    cart = request.session.get('cart', {})   
    if key in cart:
        cart[key]['qty'] -= 1
        if cart[key]['qty'] <= 0:
            del cart[key]      
    request.session['cart'] = cart
    return redirect('viewCart')


def deleteProduct(request, product_id):
    if not request.session.get('id'):
        return render('partnerLogin')
    
    product= get_object_or_404(Products, product_id=product_id)

    product.delete()
    return redirect('productList')

def editProduct(request, product_id):
    if not request.session.get('id'):
        return redirect('partnerLogin')
    
    product= get_object_or_404(Products, product_id=product_id)

    if request.method=="POST":
        product.product_name = request.POST.get('product_name')
        product.product_description = request.POST.get('product_description')
        product.product_price = request.POST.get('product_price')
        product.product_quantity = request.POST.get('product_quantity')

        if request.FILES.get('product_cover_image'):
            product.product_cover_image = request.FILES.get('product_cover_image')

        product.save()

        return redirect('productList')
    
    return render(request, 'partners/edit_product.html',{
        'product': product
    })


def contact(request):
    return render(request, 'contact.html')

def PlaceOrder(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('viewCart')
    if request.method == "POST":
        total = sum(
            item['ProductPrice'] * item['qty']
            for item in cart.values()
        )

        order = Orders.objects.create(
            user_id=1,  
            order_number=generate_order_id(),
            name=request.POST.get('cst_name'),
            phone=int(request.POST.get('cst_phone')),
            address=request.POST.get('cst_address'),
            total_amount=total,
            payment_method='Razorpay',
            payment_status='Pending',
            order_status='Pending'
        )

        for product_id, item in cart.items():
            OrderItems.objects.create(
                order_id=order.order_id,
                item_pro_id=int(product_id),       
                item_name=item['ProductName'],      
                item_price=item['ProductPrice'],    
                quantity=item['qty'],
                subtotal=item['ProductPrice'] * item['qty']
            )

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_review', order_id=order.order_id)

    return render(request, 'checkout.html')


def order_review(request, order_id):
    order = get_object_or_404(Orders, order_id=order_id)
    return render(request, "order_review.html", {"order":order})

def create_payment(request, order_id):
    order = get_object_or_404(Orders, order_id=order_id)

    if order.payment_status == "PAID":
        return redirect('order_review', order_id=order_id)
    
    if request.method == "POST":
        if not order.razorpay_order_id:
            rp_order = client.order.create({
                "amount": int(order.total_amount * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            order.razorpay_order_id = rp_order["id"]
            order.save()

        return render(request, 'payment.html', {
            "order": order,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": int(order.total_amount * 100)
        })

    return redirect('order_review', order_id=order.order_id)

@csrf_exempt
def payment_success(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid Request"}, status=400)
    data = json.loads(request.body)

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data["razorpay_order_id"],
            "razorpay_payment_id": data["razorpay_payment_id"],
            "razorpay_signature": data["razorpay_signature"]
        })

        order= Orders.objects.get(razorpay_order_id=data["razorpay_order_id"])

        order.razorpay_payment_id=data["razorpay_payment_id"]
        order.payment_status="PAID"
        order.order_status="PLACED"
        order.save()

        return JsonResponse({"status": "success"})
    
    except SignatureVerificationError:
        return JsonResponse(
            {"status": "failed", "message":"Signature verification failed"},
            status=400
        )
    
    except Orders.DoesNotExist:
        return JsonResponse(
            {"status": "failed", "message":"Order not found"},
            status=404
        )
    
def success_page(request):
    return render(request,'success.html')

def pending_orders(request):
    partner_id = request.session.get('id')

    if not partner_id:
        return redirect('partnerLogin')
    
    partner_products = Products.objects.filter(product_by=partner_id).values_list('product_id', flat=True)
    order_items = OrderItems.objects.filter(item_pro_id__in=partner_products)
    orders = Orders.objects.filter(
        order_id__in=order_items.values_list('order_id', flat=True),
        order_status='Pending'
    ).distinct()

    return render(request, 'partners/pending-orders.html', {
        'orders': orders
    })

def completed_orders(request):
    partner_id = request.session.get('id')

    if not partner_id:
        return redirect('partnerLogin')
    
    partner_products = Products.objects.filter(product_by=partner_id).values_list('product_id', flat=True)
    order_items = OrderItems.objects.filter(item_pro_id__in=partner_products)
    orders = Orders.objects.filter(
        order_id__in=order_items.values_list('order_id', flat=True),
        order_status='PLACED'
    ).distinct()

    return render(request, 'partners/pending-orders.html', {
        'orders': orders
    })

def order_details(request, orderId):
    partner_id = request.session.get('id')

    if not partner_id:
        return redirect('partnerLogin')
    orders = Orders.objects.get(order_id=orderId)
    orderItems = OrderItems.objects.filter(order_id=orderId)

    return render(request, 'partners/order-details.html', {'orders': orders,'orderitems': orderItems})

def generate_order_id():
    return str(int(time.time()))[-6:] + str(random.randint(10, 99))

# 6527 6589 0000 1005
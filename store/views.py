from django.shortcuts import render

import datetime
import json
from django.http import JsonResponse
from .models import *

# Create your views here.
# from django.template import context


def store(request):
    if request.user.is_authenticated:     # agar ro'yxatdan o'tgan foydalanuvchi bo'lsa pasdagilar bajariladi
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:                 # ro'yxatdan o'tmagan bo'lsa item va total ni 0 ga tenglab qo'yiladi
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, "store/store.html", context)


def cart(request):
    if request.user.is_authenticated:  # agar ro'yxatdan o'tgan foydalanuvchi bo'lsa pasdagilar bajariladi
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item
    else:  # ro'yxatdan o'tmagan bo'lsa item va total ni 0 ga tenglab qo'yiladi
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
        cartItems = order['get_cart_item']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)  # '/update_item/' URL dagi ma'lumotlani chiqarib beradi
    productId = data['productId']
    action = data['action']



    # Korzinkaga productlani qo'shadi
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse("Item was added", safe=False)


# Make pyment qilganda yani to'lov qilganda tepadan tushadigan chek
def processOrder(request):
    transaction_id = datetime.datetime.now().timetuple()
    data = json.loads(request.body)

    # agar ro'yxatdan o'tgan foydalanuvchi bo'lsa pasdagilar bajariladi
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])  # formni ichidagi totalni qiymatini total ga chiqazib olindi
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],

            )
    else:
        print('User is not logged in..')
    return JsonResponse("Payment complete", safe=False)
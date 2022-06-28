from django.shortcuts import render, redirect

import datetime
import json
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .models import *
from .utils import cookieCart, cartData, guestOrder

# CRUD
# from .forms import ProductForm

# Create your views here.
# from django.template import context


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, "store/store.html", context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

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


# from django.views.decorators.csrf import csrf_exempt
#
# @csrf_exempt
# Make pyment qilganda yani to'lov qilganda tepadan tushadigan chek
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    # agar ro'yxatdan o'tgan foydalanuvchi bo'lsa pasdagilar bajariladi
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])  # formni ichidagi totalni qiymatini total ga chiqazib olindi
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
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

    return JsonResponse("Payment complete", safe=False)




# CRUD #################################################


def products(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'products/products.html', context)


# def createProduct(request):
#     # Formani initsializatsiya qilish
#     productFrom = ProductForm()
#     if request.method == 'POST':
#         my_form = ProductForm(request.POST)
#         if my_form.is_valid():
#             my_form.save()
#             return redirect('store')
#
#     # Formani yuborish uchun direct ko'rinishga o'tkazish
#     form = {'productForm': productFrom}
#
#     # Templateni render qilish va unga formani yuborish
#     return render(request, 'products/create_products.html', form)


class CreateProduct(CreateView):
    model = Product
    template_name = 'products/create_products.html'
    success_url = reverse_lazy('products')
    fields = ('name', 'price', 'digital', 'image')


class UpdateProduct(UpdateView):
    model = Product
    template_name = 'products/update_products.html'
    success_url = reverse_lazy('products')
    fields = ('name', 'price', 'digital', 'image')


# def updateProduct(request, cid):
#     # Formani initsializatsiya qilish
#     product = Product.objects.get(id=cid)
#     productFrom = ProductForm(instance=product)
#
#     if request.method == 'POST':
#         my_form = ProductForm(request.POST, instance=product)
#         if my_form.is_valid():
#             my_form.save()
#             return redirect('products')
#
#     # Formani yuborish uchun direct ko'rinishga o'tkazish
#     form = {'productForm': productFrom}
#
#     # Templateni render qilish va unga formani yuborish
#     return render(request, 'products/update_products.html', form)


def deleteProduct(request, cid):
    # O'chirlgan obyekt ma'lumotlarni olish
    product = Product.objects.get(id=cid)

    if request.method == 'POST':
            product.delete()
            return redirect('products')

    # O'chirilgan ma'lumotni yuborish uchun direct ko'rinishga o'tkazish
    form = {'product': product}

    # Templateni render qilish va unga formani yuborish
    return render(request, 'products/delete_products.html', form)


class UpdateCustomer(UpdateView):
    model = User
    template_name = 'update_customer.html'
    success_url = reverse_lazy('customer')
    fields = ('username', 'email', 'first_name', 'last_name', 'is_staff')


def deleteCustomer(request, cid):
    # O'chirlgan obyekt ma'lumotlarni olish
    customer = User.objects.get(id=cid)

    if request.method == 'POST':
            customer.delete()
            return redirect('customer')

    # O'chirilgan ma'lumotni yuborish uchun direct ko'rinishga o'tkazish
    form = {'customer': customer}

    # Templateni render qilish va unga formani yuborish
    return render(request, 'delete_customer.html', form)







def customer(request):

    data = cartData(request)
    cartItems = data['cartItems']

    customers = User.objects.all()

    context = {'customers': customers, 'cartItems': cartItems}

    return render(request, 'customer.html', context)


def order(request):

    data = cartData(request)
    cartItems = data['cartItems']

    orders = Order.objects.all()
    order_total = data['order']
    context = {'orders': orders, 'cartItems': cartItems, 'order_total': order_total}

    return render(request, 'order.html', context)





def orderItem(request):

    data = cartData(request)
    cartItems = data['cartItems']

    order_items = OrderItem.objects.all()
    order_total = data['order']
    context = {'order_items': order_items, 'cartItems': cartItems, 'order_total': order_total}

    return render(request, 'store/order_item.html', context)


def home(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}

    return render(request, 'home.html', context)


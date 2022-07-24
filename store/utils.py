import json
from . models import *


def cookieCart(request):
    try:  # agart cartni o'chirib yuborilsa yoki xato bo'lsa cartni bo'sh qilib qo'yadi
        cart = json.loads(request.COOKIES['cart'])
        # print(f"viewsda, Cart:{cart}")
    except Exception as e:
        print(e)
        cart = {}
        # print("Xato, exceptga tushdi")
    # print('viewsda except, Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_item': 0, 'shipping': False}
    cartItems = order['get_cart_item']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_item'] += cart[i]['quantity']

            item = {
                "product": {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):

    if request.user.is_authenticated:  # agar ro'yxatdan o'tgan foydalanuvchi bo'lsa pasdagilar bajariladi
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_item

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    # print('User is not logged in..')

    # print('Cookie:', request.COOKIES)
    global orderItem
    name = data['form']['name']
    email = data['form']['email']

    cookiedate = cookieCart(request)
    items = cookiedate['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    if created:
        customer.name = name
        customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
        )

    return customer, order, orderItem



from django.shortcuts import render

# Create your views here.
# from django.template import context


def store(request):
    context = {}
    return render(request, "store/store.html", context)


def cart(request):
    context = {}
    return render(request, "store/cart.html", context)


def checkout(request):
    context = {}
    return render(request, "store/checkout.html", context)
from django.urls import path
from .import views

urlpatterns = [
    # Asosiy url uchun bo'sh qator sifatida qoldiring
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
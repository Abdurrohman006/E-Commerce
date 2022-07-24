from django.urls import path
from .import views

urlpatterns = [
    # Asosiy url uchun bo'sh qator sifatida qoldiring
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('home/', views.home, name='home'),

    path('products/', views.products, name='products'),
    path('create_products/', views.CreateProduct.as_view(), name='create_products'),
    path('update_products/<str:pk>', views.UpdateProduct.as_view(), name='update_products'),
    path('delete_products/<str:p_id>', views.deleteProduct, name='delete_products'),
    path('product_detail/<str:p_id>', views.product_detail, name='product_detail'),

    path('customer/', views.customer, name='customer'),
    path('update_customer/<str:pk>', views.UpdateCustomer.as_view(), name='update_customer'),
    path('delete_customer/<str:cid>', views.deleteCustomer, name='delete_customer'),

    path('order/', views.order, name='order'),
    path('order_item/', views.orderItem, name='order_item'),

    # CATEGORY
    path('cellphones/', views.cellphones, name='cellphones'),
]

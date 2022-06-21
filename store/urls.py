from django.urls import path
from .import views

urlpatterns = [
    # Asosiy url uchun bo'sh qator sifatida qoldiring
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),

    path('products/', views.products, name='products'),
    path('create_products/', views.createProduct, name='create_products'),
    path('update_products/<str:cid>', views.updateProduct, name='update_products'),
    path('delete_products/<str:cid>', views.deleteProduct, name='delete_products'),

]
from django.urls import path
from .import views

urlpatterns = [
    # Asosiy url uchun bo'sh qator sifatida qoldiring
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
]
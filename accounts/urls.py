from django.urls import path
from .import views

urlpatterns = [
    # Asosiy url uchun bo'sh qator sifatida qoldiring
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('signup/', views.signup, name='signup'),
]
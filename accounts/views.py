from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from store.models import Customer
from .forms import SignUpForm



# Create your views here.


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('store')
            # Redirect to a success page.
        else:
            messages.success(request, ('There Was An Error Logging In, Try again...'))
            return redirect('login_user')
    else:
        return render(request, 'registration/login.html', {})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # saving the registered user
            user = form.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email
            )
            messages.success(request, f'Your Account has been created! You can now log in')
            return redirect('login_user')
    else:
        form = SignUpForm()  # creates an empty form
    return render(request, 'registration/signup.html', {'form': form, })


def logout_user(request):
    logout(request)
    return redirect('store')
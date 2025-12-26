from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta
from django.conf import settings
import jwt



def home_page(request):
    return render(request, 'users/home.html')

def create_groups():
    groups = ['Admin', 'Seller', 'Buyer']
    for group in groups:
        Group.objects.get_or_create(name=group)

def register_view(request):
    create_groups()  # Create groups if they don't exist
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')  # Get the selected role
            if role:
                group = Group.objects.get(name=role)  # Assuming you've created groups for roles
                group.user_set.add(user)  # Assign user to the selected group
            return redirect('login') # Redirect to homepage after successful registration
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                payload = {
                    'user_id': user.id,
                    'role': user.groups.first().name if user.groups.exists() else 'User',  # Get user role
                    'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 mins
                    'iat': datetime.utcnow()
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                # Set the token in a HttpOnly cookie
                response = redirect('store:product_list')
                response.set_cookie('jwt', token, httponly=True)

                return response
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    response = redirect('login')
    response.delete_cookie('jwt')  # Remove JWT token cookie
    return response 

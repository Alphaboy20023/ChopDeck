from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

# from .models import Product, Cart

# Create your views here.
def index (request):
    # products = Product.objects.all()
    return render(request, 'index.html')

def menu (request):
    return render(request, 'menu.html')

def about (request):
    return render(request, 'about.html')

def blog (request):
    return render(request, 'blog.html')

def contact_us (request):
    return render(request, 'contact.html')

def register (request):
    return render(request, 'signUp.html')
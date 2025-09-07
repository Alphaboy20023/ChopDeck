from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login

# from .models import Product, Cart

# Create your views here.
def index  (request):
    # products = Product.objects.all()
    return render(request, 'index.html')
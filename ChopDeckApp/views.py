from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login


# Create your views here.

def index (request):
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')[:4]
    categories = Category.objects.all()
    return render(request, 'index.html', {'foodItems':food_items, 'categories':categories})

def menu (request):
    food_items = FoodItem.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.all()
    return render(request, 'menu.html', {'foodItems':food_items, 'categories':categories})

def menu_detail(request, pk):
    food_items = get_object_or_404(FoodItem, pk=pk)
    return render(request, 'menu-detail.html', {'food_items':food_items})

def about (request):
    return render(request, 'about.html')

def blog (request):
    blogs = Blog.objects.all()
    
    # filter by admin
    admin_blogs = blogs.filter(is_admin_post=True)
    
    # filter by users
    user_blogs = blogs.filter(is_admin_post=False)
    
    context = {
        'blogs':blogs,
        'admin_blogs':admin_blogs,
        'user_blogs':user_blogs
    }
    
    return render(request, 'blog.html', context)

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk, is_published=True)
    comments = blog.comments.filter()
    
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                blog=blog,
                author=request.user if request.user.is_authenticated else None,
                content=content
            )
            return redirect('blog-detail', pk=pk)
        
    return render(request, 'blog-detail.html', {'blog':blog, 'comments':comments})
    
@login_required(login_url='login')
def delete_blog_post(request, pk):
    if request.method == 'POST':
        author = request.user
        blogpost = get_object_or_404(Blog, pk =pk, author=author)
        blogpost.delete()
        messages.success(request, "post deleted successfully")
    return redirect('blog')

def contact_us (request):
    return render(request, 'contact.html')

def order(request, pk):
    pass

def cancel_order(request):
    pass

def food_order(request):
    pass

def payment(request, pk):
    pass

def register (request):
    if request.method == 'POST':
        username = request.POST['username'].upper()
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if len(username) < 4:
            messages.error(request, 'username must be longer than 4 characters')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'password and confirm password are not the same')
            return redirect('register')
        if len(password) < 5:
            messages.error(request, 'password must be longer than 5 characters')
            return redirect('register')
        if not email:
            messages.error(request, 'email cannot be empty')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'username already exist')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email already exists')
            
        # create new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account Created successfully')
        return redirect('login')
    return render(request, 'signUp.html') 

def login (request):
    if request.method == 'POST':
        username = request.POST['username'].upper()
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'login successful')
            return redirect('index')
        else:
            messages.error(request, 'User Does Not Exist')
    return render(request, 'login.html')
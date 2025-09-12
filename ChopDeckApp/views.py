from django.contrib import messages
from django.http import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.urls import reverse
from .cart import Cart
from django.views.decorators.http import require_POST


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
    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(FoodItem),
        object_id=food_items.id
    )
    comment_count = comments.count()
    return render(request, 'menu-detail.html', {'food_items':food_items, 'comments':comments, 'comment_count':comment_count})

def add_to_cart(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(FoodItem, id=food_id)
    quantity = int(request.POST.get("quantity", 1))
    cart.add(food=food, quantity=quantity)
    return redirect(request.META.get("HTTP_REFERER", "menu"))

def remove_from_cart(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(FoodItem, id=food_id)
    cart.remove(food)
    return redirect("cart")

def cart(request):
    cart = Cart(request)
    return render(request, "cart.html", {"cart": cart})

@require_POST
def update_cart(request, food_id):
    if request.method == "POST":
        food_id = str(food_id)
        cart = Cart(request)
        current_qty = cart.cart.get(food_id, {}).get("quantity", 0)

        if "action" in request.POST:
            if request.POST["action"] == "increment":
                new_qty = current_qty + 1
            elif request.POST["action"] == "decrement":
                new_qty = current_qty - 1
            else:
                new_qty = current_qty
        else:
            # direct input from <input type="number">
            new_qty = int(request.POST.get("quantity", current_qty))

        if new_qty > 0:
            cart.cart[food_id]["quantity"] = new_qty
        else:
            cart.remove(food_id)

        cart.save()
    return redirect("cart")


def about (request):
    return render(request, 'about.html')


def blog (request):
    blogs = Blog.objects.all()

    # filter by admin
    admin_blogs = blogs.filter(is_admin_post=True)
    user_blogs = blogs.filter(is_admin_post=False)

    context = {
        "blogs": blogs,
        "admin_blogs": admin_blogs,
        "user_blogs": user_blogs,
    }
    return render(request, "blog.html", context)
    
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk, is_published=True)
    blogs = Blog.objects.exclude(pk=pk).order_by('-created_at')[:5]
    blog_type = ContentType.objects.get_for_model(Blog)
    
    comments = Comment.objects.filter(
        content_type=blog_type,
        object_id=blog.pk
    ).order_by("-created_at")

    comment_count = comments.count()
    
    if request.method == "POST":
        content = request.POST.get('content')
        author = request.user
        if content:
            Comment.objects.create(
                content_type=blog_type,
                object_id=blog.pk,
                author=author,
                content=content
            )
        return redirect('blog-detail', pk=pk)
        
    return render(request, 'blog-detail.html', {'blog':blog, 'comments':comments, 'blogs':blogs, 'comment_count':comment_count})

@csrf_exempt
def add_comment(request):
    if request.method == "POST":
        model = request.POST.get("model")   # "blog" or "fooditem"
        object_id = request.POST.get("object_id")

        try:
            content_type = ContentType.objects.get(model=model)
            obj = content_type.get_object_for_this_type(id=object_id)
        except ContentType.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid model"}, status=400)
        except Exception:
            return JsonResponse({"success": False, "error": "Object not found"}, status=404)

        user = request.user if request.user.is_authenticated else None

        Comment.objects.create(
            content_object=obj,
            user=user,
            name=request.POST.get("name"),
            content=request.POST.get("content"),
        )

        # redirect depending on model
        if model == "blog":
            redirect_url = reverse("blog-detail", kwargs={"pk": obj.id})
        else:  # fooditem
            redirect_url = reverse("menu-details", kwargs={"pk": obj.id})

        return JsonResponse({"success": True, "redirect_url": redirect_url})

    return JsonResponse({"success": False}, status=400)
    
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

def checkout(request):
    return render(request, 'checkout.html')

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
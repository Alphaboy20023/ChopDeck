import time
from django.contrib import messages
# ni filename - creates a file
from django.http import HttpResponse 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .cart import Cart
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Q
import requests
from django.conf import settings
import json



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

def cart(request, order_id=None):
    cart = Cart(request)
    
    sub_total = sum(Decimal(item['price']) * int(item['quantity']) for item in cart)
    shipping_fee = Decimal("1000.00") if sub_total > 0 else Decimal("0.00")
    grand_total = sub_total + shipping_fee
    
    # formatting ,
    formatted_sub_total = f"₦ {intcomma(int(sub_total))}"
    formatted_shipping_fee = f"₦ {intcomma(int(shipping_fee))}"
    formatted_grand_total = f"₦ {intcomma(int(grand_total))}"
    
    return render(request, "cart.html", {
        "cart": cart,
        "sub_total":formatted_sub_total,
        "shipping_fee":formatted_shipping_fee,
        "grand_total":formatted_grand_total
        })

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

def cancel_order(request):
    pass

def checkout(request):
    cart = request.session.get('cart', {})
    
    cart_items = []
    sub_total = Decimal("0.00")
    
    for product_id, item in cart.items():
        food = FoodItem.objects.get(id=product_id)
        
        price = Decimal(item.get('price', 0))
        quantity = int(item.get('quantity', 1))
        total = price * quantity
        formatted_price = f"₦ {intcomma(int(price))}"
        formatted_total = f"₦ {intcomma(int(total))}"
        
        

        cart_items.append({
            "id": product_id,
            "title": food.title,
            "price": formatted_price,
            "quantity": quantity,
            "total": formatted_total,
            "image":food.image
        })

        sub_total += total
    
    shipping_fee = Decimal("1000.00") if sub_total > 0 else Decimal("0.00")
    grand_total = sub_total + shipping_fee
    
    
    # formatting ,
    formatted_sub_total = f"₦ {intcomma(int(sub_total))}"
    formatted_shipping_fee = f"₦ {intcomma(int(shipping_fee))}"
    formatted_grand_total = f"₦ {intcomma(int(grand_total))}"
    
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('cash', 'Cash'),
    ]
    
    success_message = None
    
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        message = request.POST.get("message")
        payment_method = request.POST.get("payment_method")

        messages.success(request, "✅ Your order has been placed successfully!")
        # save Order + Payment
        
        order = Order.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        address=address,
        total=grand_total,
        status="pending",           # or whatever default you use
        payment_status="initiated", # optional
        )
        
        print(full_name, phone, email, address, message, payment_method)
        return redirect("payment", order_id=order.id)
        
    
    context = {
        "cart_items": cart_items,
        "sub_total": formatted_sub_total,
        "shipping_fee": formatted_shipping_fee,
        "grand_total": formatted_grand_total,
        "payment_methods": PAYMENT_METHODS,
        "success_message": success_message,
    }
    
    
    return render(request, 'checkout.html', context)

def payment_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # print("PAYMENT VIEW STARTED", order_id)

    # Initialize Paystack transaction
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "amount": int(order.total * 100),  # amount in kobo
        "email": order.email,
        "reference": f"order_{order.id}_{int(time.time())}",
        "callback_url": request.build_absolute_uri(reverse('payment_callback')),
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print("PAYSTACK RESPONSE:", response_data)

        if response_data.get('status') and 'authorization_url' in response_data['data']:
            order.payment_reference = data['reference']
            order.save()
            print("Redirecting to Paystack...")
            return redirect(response_data['data']['authorization_url'])
        else:
            print("Payment initialization failed:", response_data)
            # Optionally show an error page instead of going back to checkout
            return redirect('checkout')

    except Exception as e:
        print("Error initializing Paystack payment:", e)
        return redirect('checkout')

def payment_callback(request):
    reference = request.GET.get('reference')
    
    if reference:
        # Verify payment with Paystack
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        }
        
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        print("Paystack response:", response_data)

        
        if response_data['status'] and response_data['data']['status'] == 'success':
            # Payment successful
            order = Order.objects.get(payment_reference=reference)
            order.status = 'paid'
            order.payment_status = 'completed'
            order.save()
            
            messages.success(request, "Payment successful!")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Payment failed")
            return redirect('payment_failed')
    
    return redirect('checkout')



def search_food(request):
    query = request.GET.get("q", "").strip() # dont understand
    
    food_items = FoodItem.objects.filter(is_available=True,).select_related("category")
    categories = Category.objects.all()
    
    if query:
        food_items = food_items.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query)
        )
        
    context = {
        "query":query,
        "food_items":food_items,
        "categories":categories
    }
    
    return render(request, 'search.html', context)

@csrf_exempt
def chat_proxy(request):
    if request.method == 'POST':
        try:
            user_message = json.loads(request.body).get('message', '')
            
            response = requests.post(
                'https://rasa-bot-p3ib.onrender.com/webhooks/rest/webhook',
                json={'sender': 'frontend-user', 'message': user_message},
                timeout=10
            )
            
            if response.status_code == 200:
                return JsonResponse(response.json(), safe=False)
            else:
                return JsonResponse({'error': 'Rasa service error'}, status=500)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_food_items(request):
    if request.method == 'GET':
        try:
            food_items = list(FoodItem.objects.filter(is_available=True).values('id', 'title', 'price', 'description'))
            return JsonResponse({'food_items': food_items})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

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
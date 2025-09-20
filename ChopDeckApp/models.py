from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.humanize.templatetags.humanize import intcomma
from cloudinary_storage.storage import VideoMediaCloudinaryStorage, MediaCloudinaryStorage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):

    # username = None
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{self.username}'

class TimeStampField(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

class FoodItem(TimeStampField):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='foods')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True, storage=MediaCloudinaryStorage())
    is_available = models.BooleanField(default=True)
    reviews = models.PositiveIntegerField(default=0)
    stars = models.CharField(max_length=10, null=True)
    
    @property
    def formatted_price(self):
        return f"₦{intcomma(int(self.price))}"
    
    
    
    def __str__(self):
        return self.title

class Order(TimeStampField):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    
    # ✅ Checkout details
    full_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    address = models.TextField(null=True)
    notes = models.CharField(max_length=1000, null=True)
    
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    payment_method = models.CharField(max_length=50, default='paystack')
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    @property
    def sub_total(self):
        return sum(
            item.price * item.quantity for item in self.order_items.all()
        )
        
    @property
    def shipping_fee(self):
        return 500 if self.sub_total > 1500 else 100
    
    @property
    def grand_total(self):
        return self.sub_total + self.shipping_fee
    

class OrderFood(TimeStampField):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', null=True)
    food = models.ForeignKey('FoodItem', on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # store price at order time
    
    @property
    def sub_total(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"{self.quantity} x {self.food.title} in Order #{self.order.id}"

class Blog(TimeStampField):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, storage=MediaCloudinaryStorage())
    is_published = models.BooleanField(default=False)
    
    is_admin_post = models.BooleanField(default=False)
    
    def comment_count(self):
        blog_type = ContentType.objects.get_for_model(Blog)
        return Comment.objects.filter(
            content_type=blog_type,
            object_id=self.id
        ).count()
    
    def __str__(self):
        return self.title

class Comment(TimeStampField):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    name=models.CharField(max_length=150, blank=True, null=True)
    
    # generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    
    @property
    def display_name(self):
        return self.name
    
    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username} on {self.content_object}"
        return f"Comment by {self.name or 'Anonymous'} on {self.content_object}"



class Payment(TimeStampField):
    PAYMENT_METHODS = [
        ('paystack', 'Paystack'),
        ('cash', 'Cash'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    paid_at = models.DateTimeField(auto_now_add=True)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    
    def __str__(self):
        return f"Payment for Order #{self.order.id}"


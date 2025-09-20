from django.contrib import admin
from .models import *

# Register your models here.
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'category', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    
class orderAdmin(admin.ModelAdmin):
    list_display = ()
    
class blogAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'is_admin_post')

class blogAdmin(admin.ModelAdmin):
    list_display = ('author', 'blog')  
    
admin.site.register(FoodItem, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog)
admin.site.register(OrderFood)
admin.site.register(Comment)



from django.contrib import admin
from .models import *

# Register your models here.
class FoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'category', 'price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    
class order(admin.ModelAdmin):
    list_display = ()
    
    
admin.site.register(FoodItem, FoodAdmin)
admin.site.register(Category, CategoryAdmin)
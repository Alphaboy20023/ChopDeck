# cart.py
from decimal import Decimal
from django.conf import settings
from .models import FoodItem 

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, food, quantity=1, update_quantity=False):
        food_id = str(food.id)
        if food_id not in self.cart:
            self.cart[food_id] = {"quantity": 0, "price": str(food.price)}
        if update_quantity:
            self.cart[food_id]["quantity"] = quantity
        else:
            self.cart[food_id]["quantity"] += quantity
        self.save()

    def remove(self, food_id):
        food_id = str(food_id)
        if food_id in self.cart:
            del self.cart[food_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        food_ids = self.cart.keys()
        foods = FoodItem.objects.filter(id__in=food_ids)
        for food in foods:
            item = self.cart[str(food.id)]
            item["food"] = food
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
            
            item["formatted_total_price"] = f" ₦{item['total_price']:,.2f}"
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

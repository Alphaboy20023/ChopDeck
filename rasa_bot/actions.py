import os
import sys
import django
import random
from asgiref.sync import sync_to_async

# Point to your Django project root
sys.path.append(r"C:\Users\timiv\Desktop\ChopDeckFoodApp\ChopDeck")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChopDeck.settings")
django.setup()

from ChopDeckApp.models import FoodItem
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionGetMenu(Action):
    def name(self):
        return "action_get_menu"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        # Get queryset safely inside async
        food_items = await sync_to_async(list)(FoodItem.objects.all())

        if food_items:  # list is truthy if not empty
            menu_items = [food.title for food in food_items]
            menu_str = ", ".join(menu_items)

            templates = [
                f"We’ve got {menu_str}! 🥘",
                f"Today's menu includes {menu_str} 🍗.",
                f"We currently have {menu_str}.",
                f"On the menu today: {menu_str} — fresh and hot! 🔥",
                f"You can order {menu_str}. What would you like?",
                f"We’ve got {menu_str} available today."
            ]

            response = random.choice(templates)
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, no meals available right now.")

        return []

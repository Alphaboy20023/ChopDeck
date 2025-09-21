import os
import sys
import django
import random
from asgiref.sync import sync_to_async

# print("=== DEBUG PATH INFO ===")
# print(f"Current file: {__file__}")
# print(f"Current dir: {os.path.dirname(__file__)}")
# print(f"Parent dir: {os.path.dirname(os.path.dirname(__file__))}")
# print(f"Django path: {os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ChopDeck')}")
# print(f"Python path: {sys.path}")
# print("======================")

# Get the absolute path to your Django project
# Assuming your folder structure is:
# parent_folder/
# ├── ChopDeck/          (Django project)
# └── rasa_bot/          (Rasa project with this actions.py)

current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file)
parent_dir = os.path.dirname(current_dir)
django_project_path = os.path.join(parent_dir, "ChopDeck")

# Add Django project to Python path
if django_project_path not in sys.path:
    sys.path.insert(0, django_project_path)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChopDeck.settings")

try:
    django.setup()
    from ChopDeckApp.models import FoodItem  # Import without ChopDeck prefix
    DJANGO_AVAILABLE = True
except Exception as e:
    print(f"Django setup failed: {e}")
    DJANGO_AVAILABLE = False

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetMenu(Action):
    def name(self):
        return "action_get_menu"
    
    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        if not DJANGO_AVAILABLE:
            dispatcher.utter_message(text="Sorry, menu service is temporarily unavailable.")
            return []
            
        try:
            # Get food items asynchronously
            food_items = await sync_to_async(list)(FoodItem.objects.filter(is_available=True))
            
            if food_items:
                menu_items = [food.title for food in food_items]
                menu_str = ", ".join(menu_items)
                
                templates = [
                    f"We've got {menu_str}!",
                    f"Today's menu includes {menu_str}.",
                    f"We currently have {menu_str}.",
                    f"On the menu today: {menu_str} — fresh and hot!",
                    f"You can order {menu_str}. What would you like?",
                    f"We've got {menu_str} available today."
                ]
                
                response = random.choice(templates)
                dispatcher.utter_message(text=response)
            else:
                dispatcher.utter_message(text="Sorry, no meals available right now.")
                
        except Exception as e:
            print(f"Error in ActionGetMenu: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble accessing our menu right now.")
        
        return []
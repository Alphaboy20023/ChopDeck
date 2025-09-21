import requests
import random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionGetMenu(Action):
    def name(self):
        return "action_get_menu"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        try:
            # Call Django API endpoint
            response = requests.get(
                'https://chopdeck-9afj.onrender.com/api/food-items/', 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                food_items = data.get('food_items', [])
                
                if food_items:
                    menu_items = [item['title'] for item in food_items]
                    menu_str = ", ".join(menu_items)
                    
                    templates = [
                        f"We've got {menu_str}!",
                        f"Today's menu includes {menu_str}.",
                        f"We currently have {menu_str}.",
                        f"On the menu today: {menu_str} — fresh and hot!",
                        f"You can order {menu_str}. What would you like?",
                        f"We've got {menu_str} available today."
                    ]
                    
                    response_text = random.choice(templates)
                    dispatcher.utter_message(text=response_text)
                else:
                    dispatcher.utter_message(text="Sorry, no meals available right now.")
            else:
                dispatcher.utter_message(text="Sorry, I'm having trouble accessing our menu right now.")
                
        except requests.RequestException as e:
            print(f"API request error: {e}")
            dispatcher.utter_message(text="Sorry, menu service is temporarily unavailable.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            dispatcher.utter_message(text="Sorry, I'm having trouble accessing our menu right now.")
        
        return []
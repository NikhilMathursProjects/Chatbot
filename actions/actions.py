# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []




# class ActionChargingStation(Action):

#     def name(self) -> Text:
#         return "action_charging_station"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Dummy data for charging stations
#         locations = {
#             "downtown": "Station A, 123 Main St",
#             "uptown": "Station B, 456 High St",
#             "suburbs": "Station C, 789 Park Ave"
#         }

#         user_location = tracker.get_slot("location")
#         if user_location and user_location.lower() in locations:
#             station = locations[user_location.lower()]
#             response = f"The nearest charging station in {user_location} is at {station}."
#         else:
#             response = "I couldn't find a charging station for that location. Please specify downtown, uptown, or suburbs."

#         dispatcher.utter_message(text=response)
#         return []

import requests
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, Restarted


LOCATIONS_DATA = {
    "New York": 15,
    "London": 10,
    "San Francisco": 12,
    "Berlin": 8,
    "Tokyo": 20,
    "Mumbai": 11,
}


MODEL_DATA = {
    "Tesla Model 3": {
        "battery_life": "370 miles",
        "performance": "0-60 mph in 3.1 seconds",
        "range": "353 miles",
        "price": "$39,990"
    },
    "Nissan Leaf": {
        "battery_life": "226 miles",
        "performance": "0-60 mph in 7.5 seconds",
        "range": "226 miles",
        "price": "$31,670"
    },
    "Chevy Bolt": {
        "battery_life": "259 miles",
        "performance": "0-60 mph in 6.5 seconds",
        "range": "259 miles",
        "price": "$31,995"
    }
}

class ActionFindCarInfo(Action):
    def name(self) -> str:
        return "action_find_car_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the car model from the slot
        model = tracker.get_slot("model")
        
        # Check if model is set
        if not model:
            dispatcher.utter_message(text="I don't know the model you're referring to. Could you please tell me the car model?")
            return []
        
        # Get the intent to check what information the user wants
        intent = tracker.latest_message['intent'].get('name')
        
        # Check if the model is in the data
        if model in MODEL_DATA:
            car_info = MODEL_DATA[model]
            
            # Provide the requested information based on the intent
            if intent == "ask_battery_life":
                dispatcher.utter_message(text=f"The battery life of the {model} is {car_info['battery_life']}.")
            elif intent=="ask_battery_life_specific_model":
                dispatcher.utter_message(text=f"The battery life of the {model} is {car_info['battery_life']}.")
            elif intent=="ask_performance_specific_model":
                dispatcher.utter_message(text=f"The performance of the {model} is {car_info['performance']}.")
            elif intent == "ask_performance":
                dispatcher.utter_message(text=f"The performance of the {model} is {car_info['performance']}.")
            elif intent == "ask_range":
                dispatcher.utter_message(text=f"The range of the {model} is {car_info['range']}.")
            elif intent == "ask_price":
                dispatcher.utter_message(text=f"The price of the {model} is {car_info['price']}.")
            else:
                dispatcher.utter_message(text="Sorry, I couldn't understand your question.")
        else:
            dispatcher.utter_message(text="Sorry, I don't have information for that model.")
        
        return []


class ActionFindAllCarInfo(Action):
    def name(self) -> str:
        return "action_find_all_car_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the car model from the slot
        model = tracker.get_slot("model")
        
        # Check if the model exists in the MODEL_DATA
        if model in MODEL_DATA:
            car_info = MODEL_DATA[model]
            
            # Construct a detailed response using the data
            response = (
                f"Here is the information for the {model}:\n"
                f"- Battery Life: {car_info['battery_life']}\n"
                f"- Performance: {car_info['performance']}\n"
                f"- Range: {car_info['range']}\n"
                f"- Price: {car_info['price']}"
            )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text="Sorry, I don't have information for that model.")
        
        return []



class ActionFindChargingStation(Action):
    def name(self) -> Text:
        return "action_find_charging_station"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the location entity
        location = tracker.get_slot("location")
        if not location:
            # Ask user for location if it's not provided
            dispatcher.utter_message(text="Could you specify the location?")
            return []
        if location in LOCATIONS_DATA:
            count = LOCATIONS_DATA[location]
            dispatcher.utter_message(text=f"There are {count} charging stations in {location}.")
        else:
            dispatcher.utter_message(text=f"Sorry, I don't have data for charging stations in {location}.")
        
        return []


class ActionAskLocation(Action):
    def name(self) -> str:
        return "action_ask_location"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        location = tracker.get_slot("location")
        
        if not location:
            dispatcher.utter_message(text="Could you specify the location?")
            return []
        else:
            dispatcher.utter_message(text=f"Location already set to {location}")
            return []
        
class ActionAskModel(Action):
    def name(self) -> str:
        return "action_ask_model"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        model = tracker.get_slot("model")
        
        if not model:
            dispatcher.utter_message(text="Could you specify the model?")
            return []
        else:
            dispatcher.utter_message(text=f"Model already set to {model}")
            return []
        



class ActionRefreshConversation(Action):
    def name(self) -> str:
        return "action_refresh_conversation"

    def run(self,dispatcher: CollectingDispatcher, tracker, domain):
        # Collect all slots that are set (non-default)
        set_slots = [
            SlotSet(slot, value) 
            for slot, value in tracker.slots.items() 
            if value is not None and value != ""
        ]
        
        # Restart the conversation and preserve non-default slots
        return [Restarted()] + set_slots
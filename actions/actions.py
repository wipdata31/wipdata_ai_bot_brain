# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
import requests
import json

def create_appointment(name, age, symptom, mobile):
    request_url = f"http://localhost:5000/api/appointment"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "name": name, 
        "mobile": mobile, 
        "age": age, 
        "symptom": symptom
        }

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

class AskForSlotAction(Action):
    def name(self) -> Text:
        return "action_utter_ask_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        dispatcher.utter_message(text="Provide the updated " + tracker.slots.get("slot"))
        return []

class UpdateSlotAction(Action):
    def name(self) -> Text:
        return "action_update_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text")
        return [SlotSet(tracker.slots.get("slot"), value)]

class AppointmentSubmit(Action):

    def name(self) -> Text:
        return "action_utter_submit"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.slots.get("name")
        mobile = tracker.slots.get("mobile")
        age = tracker.slots.get("age")
        symptom = tracker.slots.get("symptom")
        res = create_appointment(name, mobile, age, symptom)

        if res.json()['_id']:
            dispatcher.utter_message(text="Appointment is successfully submitted. Your appointment id is " + res.json()['_id'] + ". Please store it for further use. Can I help you with anything else?")
            #value = None
            # return: 
            #     tracker.slots[mobile]=value
            #     tracker.slots[age]=value
            #     tracker.slots[symptom]=value
            # return [SlotSet(mobile, value),
            #         SlotSet(age, value),
            #         SlotSet(symptom, value)]
        else:
            dispatcher.utter_message(text="Creating Appointment is unsuccessfull")
        
        print(res.json())

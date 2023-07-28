# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
import json
from actions.func import create_appointment, get_procedures, get_states, get_cheapers, get_cities, get_avg, get_department, get_doctor, get_schedule, get_medicines, create_order
from datetime import datetime

class AskForSlotAction(Action):
    def name(self) -> Text:
        return "action_utter_ask_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        if tracker.slots.get("slot") == 'department':
            res = get_department()
            dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= tracker.slots.get("slot")
            )
        elif tracker.slots.get("slot") == 'doctor':
            department = tracker.slots.get("department")
            res = get_doctor(department)
            dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= tracker.slots.get("slot")
            )
        elif tracker.slots.get("slot") == 'schedule':
            doctor = tracker.slots.get("doctor")
            res = get_schedule(doctor)
            dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'datepicker',
                entity_name= tracker.slots.get("slot")
            )
        else:
            dispatcher.utter_message(text="Provide the updated " + tracker.slots.get("slot"))
        return []

# class UpdateSlotAction(Action):
#     def name(self) -> Text:
#         return "action_update_slot"

#     def run(
#         self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
#     ) -> List[Text]:
#         value = tracker.latest_message.get("text")
#         return [SlotSet(tracker.slots.get("slot"), value)]

class UpdateNameSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").lower().replace("namehide ", "").replace(" my name is ", "").replace(" i am ", "").replace(" call me ", "").replace(" i am known as ", "").upper()
        return [SlotSet('name', value)]

class UpdateSDOSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_scheduledateone"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").replace("scheduleDateonee ", "")
        return [SlotSet('scheduledateone', value)]

class UpdateSDTSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_scheduledatetwo"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").replace("scheduleDatetwoo ", "")
        return [SlotSet('scheduledatetwo', value)]

class UpdateDoctorSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_doctor"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").lower().replace("doctorr ", "").replace(" doctor's name is ", "").replace(" doctor ", "").replace(" doctors name ", "").upper()
        return [SlotSet('doctor', value)]

class UpdateEnquirySlotAction(Action):
    def name(self) -> Text:
        return "action_tell_enquiry"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").replace("enquiryy ", "")
        return [SlotSet('enquiry', value)]

class UpdateSymptompSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_symptomp"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").replace("symptompp ", "")
        return [SlotSet('symptomp', value)]

class UpdateEmailSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_email"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").lower().replace("emaill ", "").replace(" my email is ", "").replace(" patient's email is ", "").replace(" email ", "").replace(" patients email is ", "")
        return [SlotSet('email', value)]

def validate_ic_with_dob(ic_number, date_of_birth):
    # Ensure ic_number and date_of_birth are strings
    ic_number = str(ic_number)
    date_of_birth = str(date_of_birth)

    # Check if ic_number and date_of_birth have the correct lengths
    if len(ic_number) != 12:
        return False

    # Extract DD, MM, and YY from the IC number
    dd = ic_number[:2]
    mm = ic_number[2:4]
    yy = ic_number[4:6]

    # Construct the birthdate in the format dd/mm/yyyy
    birthdate_from_ic = f"{dd}/{mm}/{yy}"
    check_date = datetime.strptime(date_of_birth, "%d/%m/%Y").strftime("%d/%m/%y")
    # Compare the IC's birthdate with the provided date_of_birth
    if birthdate_from_ic != check_date:
        return False

    # IC number and date of birth match, return True
    return True

class UpdateICNumSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_icnum"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").replace("icnumber ", "").replace(" ic number is ", "").replace(" ic number ", "")
        nationality = tracker.slots.get("nationality")
        dob = tracker.slots.get("dob")
        
        if nationality == 'malaysian':
            if validate_ic_with_dob(value.replace('-', '').replace(' ', ''), dob):
                return [SlotSet('icnum', value)]
            else:
                print("incorrect IC.")
                dispatcher.utter_message(text="Sorry, the IC number is incorrect. Please provide the valid IC number.")
                return [SlotSet('icnum', None)] 
        else:
            return [SlotSet('icnum', value)]

class UpdateICNumSlot1Action(Action):
    def name(self) -> Text:
        return "action_tell_icnum_appointment"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        nationality = tracker.slots.get("nationality")
        dob = tracker.slots.get("dob")
        value = tracker.latest_message.get("text").replace("appoiic ", "").replace(" ic number is ", "").replace(" ic number ", "")
        
        if nationality == 'malaysian':
            if validate_ic_with_dob(value.replace('-', '').replace(' ', ''), dob):
                return [SlotSet('icnum', value)]
            else:
                print("incorrect IC.")
                dispatcher.utter_message(text="Sorry, the IC number is incorrect. Please provide the valid IC number.")
                return [SlotSet('icnum', None)] 
        else:
            return [SlotSet('icnum', value)]

def validate_date_format(date_str):
    try:
        # Attempt to parse the date string using the specified format
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        # If the date string is not in the correct format, ValueError will be raised
        return False

class UpdateDOBSlotAction(Action):

    def name(self) -> Text:
        return "action_tell_dob"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").lower().replace("dateofbirth ", "").replace(" date of birth is ", "").replace(" patient's date of birth is ", "").replace(" patient date of birth is ", "")

        if validate_date_format(value):
            # The date format is valid
            return [SlotSet('dob', value)]
        else:
            print("incorrect date.")
            # The date format is invalid
            dispatcher.utter_message(text="Sorry, the date format is incorrect. Please provide the date in the format DD/MM/YYYY.")
            return [SlotSet('dob', None)] 

class UpdateFullNameSlotAction(Action):
    def name(self) -> Text:
        return "action_tell_full_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Text]:
        value = tracker.latest_message.get("text").lower().replace("fullname ", "").replace(" patient's name is ", "").replace(" patient name is ", "").upper()
        return [SlotSet('full_name', value)]

class GetDepartments(Action):

    def name(self) -> Text:
        return "action_utter_department"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptom = tracker.slots.get("symptom")
        res = await get_department(symptom)
        if res:
            print(res.json()[0])
            dispatcher.utter_message(
            response= "utter_ask_department",
            procedures= res.json(),
            type= 'custom_text',
            entity_name= 'Department'
            )
            return [SlotSet('department', res.json()[0])]
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetDepartmentsDrop(Action):

    def name(self) -> Text:
        return "action_utter_department_drop"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        symptom = 'none'
        res = await get_department(symptom)
        if res:
             dispatcher.utter_message(
                response= "utter_ask_department_drop",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= 'Department'
             )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetDoctor(Action):

    def name(self) -> Text:
        return "action_utter_doctor"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        department = tracker.slots.get("department")
        res = await get_doctor(department)

        if res:
             dispatcher.utter_message(
                response= "utter_ask_doctor",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= 'Doctor'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetSchedule(Action):

    def name(self) -> Text:
        return "action_utter_schedule"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        doctor = tracker.slots.get("doctor")
        res = get_schedule(doctor)

        if res:
             dispatcher.utter_message(
                response= "utter_ask_schedule",
                procedures= res.json(),
                type= 'datepicker',
                entity_name= 'Schedule'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class ValidateAppointmentForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_appointment_form"

    def validate_age(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate age value."""
        print(len(slot_value))
        if ((len(slot_value) < 4) and (tracker.slots.get("requested_slot") == 'age')):
            # validation succeeded, set the value of the "age" slot to value
            return {"age": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            return {"age": None}
    def validate_mobile(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,) -> Dict[Text, Any]:
        """Validate mobile value."""
        print(len(slot_value))
        
        if len(slot_value) > 9:
            # validation succeeded, set the value of the "mobile" slot to value
            return {"mobile": slot_value}
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(response="utter_wrong_num_mobile")
            return {"mobile": None}

class AppointmentSubmit(Action):

    def name(self) -> Text:
        return "action_utter_submit"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.slots.get("name")
        mobile = tracker.slots.get("mobile")
        age = tracker.slots.get("age")
        gender = tracker.slots.get("gender")
        symptom = tracker.slots.get("symptom")
        date = tracker.slots.get("date")
        time = tracker.slots.get("time")
        department = tracker.slots.get("department")
        doctor = tracker.slots.get("doctor")
        schedule = tracker.slots.get("schedule")
        res = create_appointment(name, age, gender, symptom, date, time, mobile, department, doctor, schedule )

        if res.json()['_id']:
            dispatcher.utter_message(text="Appointment is successfully submitted. Your appointment id is " + res.json()['_id'] + ". Please store it for further use. <br/> Can I help you with anything else?")
        else:
            dispatcher.utter_message(text="Creating Appointment is unsuccessfull")
        
        print(res.json())

class GetProcedures(Action):

    def name(self) -> Text:
        return "action_utter_procedure"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        res = get_procedures()

        if res:
            # dispatcher.utter_message(text="Type any one procedure's name from below to select.\n" + ', '.join([str(elem) for elem in res.json()]))
            print(res.json())
            dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= 'Procedure'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")
        
        #print(res.json())

class GetStates(Action):

    def name(self) -> Text:
        return "action_utter_state"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        res = get_states()

        if res:
             dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= 'State'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetCities(Action):

    def name(self) -> Text:
        return "action_utter_city"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        state = tracker.slots.get("state")
        res = get_cities(state)

        if res:
             dispatcher.utter_message(
                response= "utter_drop_value",
                procedures= res.json(),
                type= 'dropdown',
                entity_name= 'City'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetCheaperCity(Action):

    def name(self) -> Text:
        return "action_utter_cheaper_city"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        procedure = tracker.slots.get("procedure")
        state = tracker.slots.get("state")
        city = tracker.slots.get("city")
        res = get_cheapers(procedure, state, city)
        print(res.json())
        if res:
            dispatcher.utter_message(
                response= "utter_report",
                procedures= res.json(),
                type= 'report',
                entity_name= 'Cheaper City'
            )          
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetCheaperProvider(Action):

    def name(self) -> Text:
        return "action_utter_cheaper_provider"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        procedure = tracker.slots.get("procedure")
        state = tracker.slots.get("state")
        city = tracker.slots.get("city")
        res = get_cheapers(procedure, state, city)
        print(res.json())
        print(procedure, state, city)
        if res:
            dispatcher.utter_message(
                response= "utter_report",
                procedures= res.json(),
                type= 'report',
                entity_name= 'Cheaper Provider'
            )  
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetAverageCharge(Action):

    def name(self) -> Text:
        return "action_utter_average_charge"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        procedure = tracker.slots.get("procedure")
        state = tracker.slots.get("state")
        city = tracker.slots.get("city")
        res = get_avg(procedure, state, city, 1)
        print(res.json())
        print(procedure, state, city)
        if res:
            dispatcher.utter_message(
                response= "utter_report",
                procedures= res.json(),
                type= 'report',
                entity_name= 'Average Charge'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class GetAverageMedicare(Action):

    def name(self) -> Text:
        return "action_utter_average_medicare"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        procedure = tracker.slots.get("procedure")
        state = tracker.slots.get("state")
        city = tracker.slots.get("city")
        res = get_avg(procedure, state, city, 0)
        print(res.json())
        print(procedure, state, city)
        if res:
            dispatcher.utter_message(
                response= "utter_report",
                procedures= res.json(),
                type= 'report',
                entity_name= 'Average Medicare Charge'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class CheckRefills(Action):

    def name(self) -> Text:
        return "action_check_for_refills"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        userId = tracker.sender_id
        res = get_medicines(userId)
        print(res.json())
        if res:
            dispatcher.utter_message(
                response= "utter_general_custom",
                procedures= res.json(),
                type= 'carosel',
                entity_name= 'Medicines for refill'
            )
        else:
            dispatcher.utter_message(text="request unsuccessfull")

class SubmitRefillRequest(Action):

    def name(self) -> Text:
        return "action_submit_refill_request"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        userId = tracker.sender_id
        refill_items = tracker.slots.get("refill_items")
        res = create_order(userId, refill_items)

        if res.json()['_id']:
            dispatcher.utter_message(text="Order is successfully placed to your medicine provider. Your order id is " + res.json()['_id'] + ". Please store it for further use. You will get a notification when the order will be started to process. <br/><br/> Can I help you with anything else?")
        else:
            dispatcher.utter_message(text="Creating Order is unsuccessfull")
        
        print(res.json())
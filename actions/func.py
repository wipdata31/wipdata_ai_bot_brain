import os
import requests
import json

# baseUrl = 'http://localhost:5000'
# baseUrl = 'https://aibotapis.azurewebsites.net'
baseUrl = 'http://35.247.186.176:5000'
baseUrl2 = 'http://34.126.128.236:5000'

def make_reg(full_name, mykad, date_from, date_to, visit_person):
    request_url = f"{baseUrl2}/api/ptpscrape/createPTPreg"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "full_name": full_name, 
        "mykad": mykad, 
        "date_from": date_from, 
        "date_to": date_to, 
        "visit_person": visit_person
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

def create_appointment(name, age, gender, symptom, date, time, mobile, department, doctor, schedule):
    request_url = f"{baseUrl}/api/appointment"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "name": name, 
        "mobile": mobile, 
        "age": age, 
        "gender": gender, 
        "symptom": symptom,
        "department": department,
        "doctor": doctor,
        "schedule":  f"{date}, {time}"
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


async def get_department(symptom):
    request_url = f"{baseUrl}/api/doctor/getDept/{','.join(symptom)}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


async def get_doctor(department):
    request_url = f"{baseUrl}/api/doctor/getDoctor/{department}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_schedule(doctor):
    request_url = f"{baseUrl}/api/doctor/getSchedule/{doctor}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response of schedule status code: {response}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_procedures():
    request_url = f"{baseUrl}/api/mediData/getProcedures"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_states():
    request_url = f"{baseUrl}/api/mediData/getStates"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_cheapers(procedure, state, city):
    request_url = f"{baseUrl}/api/mediData/getCheapers"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    data = {
        "procedure": procedure, 
        "state": state, 
        "city": city
        }
    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_cities(state):
    request_url = f"{baseUrl}/api/mediData/getCities/{state}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_avg(procedure, state, city, charges):
    request_url = f"{baseUrl}/api/mediData/getAvg"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    print(procedure, state, city, charges)
    data = {
        "procedure": procedure, 
        "state": state, 
        "city": city,
        "charges": charges
        }
    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def get_medicines(userId):
    request_url = f"{baseUrl}/api/user/getMedicines/182.48.77.87"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


def create_order(userId, refill_items):
    request_url = f"{baseUrl}/api/appointment"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "name": userId, 
        "mobile": '999',
        "symptom": refill_items,
        "department": 'medicine_refill'
        }

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")
        return response
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    except requests.exceptions.ConnectionError: 
        ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))


    #for running the githube action. no use of this code bloc
    def no_use_1(userId, refill_items):
        request_url = f"{baseUrl}/api/appointment"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        data = {
            "name": userId, 
            "mobile": '999',
            "symptom": refill_items,
            "department": 'medicine_refill'
            }

        try:
            response = requests.post(
                request_url, headers=headers, data=json.dumps(data)
            )
            response.raise_for_status()
            print(f"Response status code: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.ConnectionError: 
            ('Connection aborted.', OSError(107, 'Transport endpoint is not connected'))

import os
import requests
import json

baseUrl = 'http://localhost:5000'

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


def get_department():
    request_url = f"{baseUrl}/api/doctor/getDept"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

def get_doctor(department):
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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response of schedule status code: {response}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

def get_medicines(userId):
    request_url = f"{baseUrl}/api/user/getMedicines/{userId}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    try:
        response = requests.get(
            request_url, headers=headers
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response

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
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(f"Response status code: {response.status_code}")
    return response
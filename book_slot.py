#!/usr/bin/env python

import csv, json, http.client, os
from sys import platform

from variables import *

def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

conn = http.client.HTTPSConnection("cdn-api.co-vin.in")

booked_slot = dict()

file_name = 'available_slots.csv'
# for windows os, provide the absolute path
if check_os() == 3:
  file_name = '{}\\available_slots.csv'.format(WINDOWS_ABSOLUTE_PATH)

reader = csv.DictReader(open(file_name, 'r'))
for slot_info in reader:
  if slot_info.get('Book This') == '1':
    booked_slot = slot_info

if not booked_slot:
  print("No slot selected. Please enter 1 for the selected slot in the \"Book This\" column of available_slots.csv file. Also make sure to add captcha in the captcha column")
  raise Exception("No slot selected")

beneficiaries = [
  # "28979499715650",
]

# Get the session and center details from the available_slots.csv file
request_data = {
  "center_id": int(booked_slot.get('Center ID')),
  "session_id": booked_slot.get('Session Id'),
  "slot": booked_slot.get('Slot'),
  "captcha": booked_slot.get('Captcha'),
  "beneficiaries": BENEFICIARIES,
  "dose": VACCINE_DOSE,
}
payload = json.dumps(request_data)

print("Booking slot ::")
print(json.dumps(request_data, indent=4))

file_name = "token.txt"
# for windows os, provide the absolute path
if check_os() == 3:
  file_name = '{}\\token.txt'.format(WINDOWS_ABSOLUTE_PATH)

with open(file_name) as f:
    content = f.readlines()

token = content[0]

headers = {
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'Accept': 'application/json, text/plain, */*',
  'Referer': 'https://selfregistration.cowin.gov.in/',
  'Authorization': 'Bearer {}'.format(token),
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'Content-Type': 'application/json'
}

conn.request("POST", "/api/v2/appointment/schedule", payload, headers)
resp = conn.getresponse()

data = resp.read()
response_data = json.loads(data)

print(response_data)

import json, os, http.client, csv
from sys import platform
from collections import OrderedDict
from datetime import datetime, timedelta

from variables import *

# -------------------------Book Slot----------------------------
def book_slot(slot_info):

  session_id = slot_info.get('Session Id')
  center_id = slot_info.get('Center ID')
  slot = slot_info.get('Slot')

  request_data = {
    "center_id": int(center_id),
    "session_id": session_id,
    "slot": slot,
    "captcha": GENERATED_CAPTCHA,
    "beneficiaries": BENEFICIARIES,
    "dose": VACCINE_DOSE,
  }

  payload = json.dumps(request_data)
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

# -------------------------Fetch sessions available-------------
def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

if len(DIRECT_BOOKING_PREFERRED_CENTERS) == 0 and len(DIRECT_BOOKING_EXCLUDE_CENTERS) == 0:
  print("No pre-filtered/pre-excluded centers found")
  exit()

today = datetime.today().strftime('%d-%m-%Y')

file_name = "token.txt"
# for windows os, provide the absolute path
if check_os() == 3:
  file_name = '{}\\token.txt'.format(WINDOWS_ABSOLUTE_PATH)

with open(file_name) as f:
    content = f.readlines()

token = content[0]

conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
payload = ''
headers = {
  'authority': 'cdn-api.co-vin.in',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'Authorization': 'Bearer {}'.format(token),
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'origin': 'https://www.cowin.gov.in',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.cowin.gov.in/',
  'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
}

conn.request("GET", "/api/v2/appointment/sessions/calendarByPin?pincode={}&date={}".format(PINCODE, today), payload, headers)

res = conn.getresponse()

if res.status != 200:
  print("Exception raised :: {}, reason :: {}".format(res.status, res.reason))
  raise Exception(res)

data = res.read()
response_data = json.loads(data)

centers = response_data.get('centers')

if VACCINE_DOSE == 1:
  capacity_key = 'available_capacity_dose1'
else:
  capacity_key = 'available_capacity_dose2'

for data in centers:
  if data.get("center_id") in CENTERS_TO_IGNORE:
    continue;
  if len(PREFERRED_CENTERS) > 0 and data.get("center_id") not in PREFERRED_CENTERS:
    continue;

  for session in data.get("sessions"):
   # for 2nd dose, check the vaccine
    if VACCINE_DOSE == 2 and session.get("vaccine") != DOSE_2_VACCINE:
      continue;
    if session.get("min_age_limit") == MIN_AGE_LIMIT and session.get(capacity_key) > 0:
      slot_info = OrderedDict()
      # booking the second slot for easy commute
      slot_info['Slot'] = session.get('slots')[1]
      slot_info['Center ID'] = data.get("center_id")
      slot_info['Session Id'] = session.get('session_id')
      book_slot(slot_info)

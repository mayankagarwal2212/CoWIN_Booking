#!/usr/bin/python

import json, os, http.client, csv, datetime
from sys import platform
from collections import OrderedDict

from variables import *

def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

# The notifier function
def notify(title, message):

    os_type = check_os()
    if os_type == 2:
      os.system("osascript -e 'display notification \"{}\" with title \"{}\" sound name \"default\"'".format(message, title))
    # for linux based systems
    elif os_type == 1:
      os.system("notify-send Vaccine-Slot-Available '{}'".format(message))
    # uncomment below for windows user
    else:
      from win10toast import ToastNotifier
      toaster = ToastNotifier()
      toaster.show_toast(title, message)

def get_available_slots(today):

  available_slots = list()

  conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
  payload = ''
  headers = {
    'authority': 'cdn-api.co-vin.in',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'origin': 'https://www.cowin.gov.in',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.cowin.gov.in/',
    'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
  }

  if PINCODE:
    conn.request("GET", "/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(PINCODE, today), payload, headers)    
  else:
    conn.request("GET", "/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}".format(DISTRICT_ID, today), payload, headers)

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
      if session.get("min_age_limit") == MIN_AGE_LIMIT and session.get(capacity_key) > 1:
        for slot in session.get('slots'):
          slot_info = OrderedDict()
          slot_info['Center Name'] = data.get("name")
          slot_info['Center Address'] = data.get("address")
          slot_info['Block Name'] = data.get("block_name")
          slot_info['Vaccine'] = session.get("vaccine")
          slot_info['Date'] = session.get("date")
          slot_info['Slot'] = slot
          slot_info['Fee Type'] = data.get("fee_type")
          slot_info['Doses'] = session.get('available_capacity_dose1')
          slot_info['Center ID'] = data.get("center_id")
          slot_info['Session Id'] = session.get('session_id')
          available_slots.append(slot_info)

  return available_slots

def send_whatsapp_notification(message):
  from twilio.rest import Client

  client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
  from_whatsapp_number='whatsapp:{}'.format(TWILIO_MOBILE_NUMBER)
  to_whatsapp_number='whatsapp:{}'.format(TO_WHATSAPP_NUMBER)

  client.messages.create(body=message,
                         from_=from_whatsapp_number,
                         to=to_whatsapp_number)

available_slots = list()
available_slots += get_available_slots(datetime.datetime.today().strftime('%d-%m-%Y'))
available_slots += get_available_slots((datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%d-%m-%Y'))

file_name = 'available_slots.csv'
if check_os() == 3:
  file_name = '{}\\available_slots.csv'.format(WINDOWS_ABSOLUTE_PATH)

f = open(file_name, "w")

if len(available_slots) > 0:
    headers = list(available_slots[0].keys())

    dict_writer = csv.DictWriter(f, headers)
    dict_writer.writeheader()
    dict_writer.writerows(available_slots)

    # sent alert to user
    for slot_info in available_slots:
      alert_message = ""
      for key, value in slot_info.items():
        alert_message += "{}: {} | ".format(key, value)
      notify(title='CoWIN slot available', message=alert_message)

      if SEND_WHATSAPP_ALERT:
        send_whatsapp_notification(alert_message)

f.close()

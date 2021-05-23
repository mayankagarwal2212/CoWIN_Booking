#!/usr/bin/python

import json, os, http.client, csv, datetime
from sys import platform
from collections import OrderedDict

# uncomment below if whatsapp notification enabled
# from twilio.rest import Client

# uncomment below for windows 10 user
# from win10toast import ToastNotifier

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
    # else:
    #   toaster = ToastNotifier()
    #   toaster.show_toast(title, message)

def get_available_slots(today):

  available_slots = list()

  # To search by District
  # update the district id in the url
  # url = "Request URL: https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=257&date={}".format(today)

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

  # Search by PIN
  # update the pincode
  pincode = 826001
  conn.request("GET", "/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode, today), payload, headers)

  # To search by District
  # update the district id in the url
  # url = "Request URL: https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=257&date={}".format(today)
  # conn.request("GET", "/api/v2/appointment/sessions/public/calendarByDistrict?district_id=257&date={}".format(today), payload, headers)

  res = conn.getresponse()

  if res.status != 200:
    print("Exception raised :: {}".format(res.status))
    raise Exception(res)

  data = res.read()
  response_data = json.loads(data)

  # age limit preference for alert
  # for 45*, min_age_limit = 45
  # for 18*, min_age_limit = 18
  min_age_limit = 18
  centers = response_data.get('centers')

  # centers to exclude for alert
  ignore_centers = [
    # 701780,
    # 618194,
  ]
  preferred_centers = [
    # 701780,
    # 618194,
  ]
  for data in centers:
    if data.get("center_id") in ignore_centers:
      continue;
    if len(preferred_centers) > 0 and data.get("center_id") not in preferred_centers:
      continue;
    for session in data.get("sessions"):
      # available_capacity_dose1 => For 1st dose alert
      # available_capacity_dose2 => For 2nd dose alert
      if session.get("min_age_limit") == min_age_limit and session.get("available_capacity_dose1") > 1:
        for slot in session.get('slots'):
          slot_info = OrderedDict()
          slot_info['Book This'] = ''
          slot_info['Captcha'] = ''
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

# uncomment below method if whatsapp notification enabled

# def send_whatsapp_notification(message):
#   # Register in twilio and update the SID and token
#   # Reference: https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out.

#   account_sid = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
#   auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"

#   client = Client(account_sid, auth_token)
#   # this is the Twilio sandbox testing number
#   from_whatsapp_number='whatsapp:+141XXXXXXXX'
#   # replace this number with your own WhatsApp Messaging number
#   to_whatsapp_number='whatsapp:+91810XXXXXX'

#   client.messages.create(body=message,
#                          from_=from_whatsapp_number,
#                          to=to_whatsapp_number)

available_slots = list()
available_slots += get_available_slots(datetime.datetime.today().strftime('%d-%m-%Y'))
available_slots += get_available_slots((datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%d-%m-%Y'))

# enable this once the twilio account is configured
send_whatsapp_alert = False

f = open('available_slots.csv', "w")

if len(available_slots) > 0:
    headers = list(available_slots[0].keys())

    dict_writer = csv.DictWriter(f, headers)
    dict_writer.writeheader()
    dict_writer.writerows(available_slots)

    # sent alert to user
    for slot_info in available_slots:
      alert_message = ""
      slot_info.pop("Book This", None)
      slot_info.pop("Captcha", None)
      for key, value in slot_info.items():
        alert_message += "{}: {} | ".format(key, value)
      notify(title='CoWIN slot available', message=alert_message)

      # uncomment below if whatsapp notification enabled
      # if send_whatsapp_alert:
      #   send_whatsapp_notification(alert_message)

f.close()

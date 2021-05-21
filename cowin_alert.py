#!/usr/bin/python

import requests, json, os
from sys import platform
import datetime
# uncomment this if whatsapp notification enabled
# from twilio.rest import Client
# uncomment this for windows user
# from win10toast import ToastNotifier

def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

# The notifier function
def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)

    os_type = check_os()
    if os_type == 2:
      os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s])))
    # for linux based systems
    elif os_type == 1:
      os.system("notify-send Vaccine-Slot-Available '{}'".format(message))
    # uncomment this for windows user
    # else:
    #   toaster = ToastNotifier()
    #   toaster.show_toast(title, message)

def get_available_slots(today):

  available_slots = list()
  # Search by PIN
  # update the pincode in the url
  url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=826001&date={}".format(today)

  # To search by District
  # update the district id in the url
  # url = "Request URL: https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=257&date={}".format(today)

  payload={}
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

  response = requests.request("GET", url, headers=headers, data=payload)

  if response.status_code != 200:
    print("Exception raised :: {}".format(response._content))
    raise Exception(response)

  response_data = json.loads(response._content)

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
      center_details = "{}, {}, {}, {}\nCenter id :: {}".format(data.get('name'), data.get("address"), data.get("block_name"), data.get("fee_type"), data.get("center_id"))
      # available_capacity_dose1 => For 1st dose alert
      # available_capacity_dose2 => For 2nd dose alert
      if session.get("min_age_limit") == min_age_limit and session.get("available_capacity_dose1") > 1:
        session_data = "Vaccine available :: {}\nDate :: {}\nCapacity :: {}".format(session.get("vaccine"), session.get("date"), session.get('available_capacity_dose1'))
        slots = ', '.join(session.get('slots'))
        session_data += "\nSession id: {}\nSlots :: {}".format(session.get('session_id'), slots)
        available_slots.append("{}\n{}".format(center_details, session_data))

  return available_slots

# uncomment this if whatsapp notification enabled

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
f = open("available_slots.txt", "w")
if len(available_slots) > 0:
  # to open iterm in the iOS
  f.write("\n")
  for slot_details in available_slots:
    f.write(slot_details)
    f.write("\n\n")

    alert_message = slot_details.replace("\n", " | ")
    notify(title    = 'CoWIN slot available',
       subtitle = "",
       message  = alert_message)

    # uncomment this if whatsapp notification enabled
    # if send_whatsapp_alert:
    #   send_whatsapp_notification(alert_message)

  # for iOS systems
  if check_os() == 2:
    os.system("open -a iTerm .")
  else:
    os.system("gnome-terminal")

f.close()

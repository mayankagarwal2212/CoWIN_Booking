#!/usr/bin/python

import requests, json, os
from sys import platform
from datetime import datetime

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
    # for iOS systems
    if check_os() == 2:
      os.system('/usr/local/bin/terminal-notifier {}'.format(' '.join([m, t, s])))
    # for linux based systems
    else:
      os.system("notify-send Vaccine-Slot-Available '{}'".format(message))

today=datetime.today().strftime('%d-%m-%Y')

# update the pincode in the url
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=826001&date={}".format(today)

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
available_slots = list()
for data in centers:
  if data.get("center_id") in ignore_centers:
    continue;
  if len(preferred_centers) > 0 and data.get("center_id") not in preferred_centers:
    continue;
  for session in data.get("sessions"):
    center_details = "{}, {}, {}, {}\nCenter id :: {}".format(data.get('name'), data.get("address"), data.get("block_name"), data.get("fee_type"), data.get("center_id"))
    if session.get("min_age_limit") == min_age_limit and session.get("available_capacity_dose1") > 1:
      session_data = "Vaccine available :: {}\nDate :: {}\nCapacity :: {}".format(session.get("vaccine"), session.get("date"), session.get('available_capacity_dose1'))
      slots = ', '.join(session.get('slots'))
      session_data += "\nSession id: {}\nSlots :: {}".format(session.get('session_id'), slots)
      available_slots.append("{}\n{}".format(center_details, session_data))

f = open("available_slots.txt", "w")
if len(available_slots) > 0:
  # to open iterm in the iOS
  f.write("\n")
  for slot_details in available_slots:
    f.write(slot_details)
    f.write("\n\n")

    # send alert on the iOS
    notify(title    = 'CoWIN slot available',
       subtitle = "",
       message  = slot_details)

  # for iOS systems
  if check_os() == 2:
    os.system("open -a iTerm .")
  else:
    os.system("gnome-terminal")

f.close()

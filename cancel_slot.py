#!/usr/bin/env python

import json
import http.client
from sys import platform

from variables import *


def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

url = "https://cdn-api.co-vin.in/api/v2/appointment/cancel"
conn = http.client.HTTPSConnection("cdn-api.co-vin.in")

payload = json.dumps({
  "appointment_id": BOOKED_APPOINTMENT_ID,
  "beneficiariesToCancel": BENEFICIARIES
})

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

conn.request("POST", "/api/v2/appointment/cancel", payload, headers)
resp = conn.getresponse()
data = resp.read()

if resp.status == 200:
  print("Appointment canceled")
else:
  print(data)

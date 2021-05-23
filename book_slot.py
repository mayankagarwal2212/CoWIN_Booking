#!/usr/bin/env python

import json
import http.client

conn = http.client.HTTPSConnection("cdn-api.co-vin.in")

# Get the session and center details from the available_slots.txt file
center_id = 701792
session_id = "0edb6bde-a57c-4b42-9dd4-85f177183c47"
slot_time = "10:00AM-11:00AM"
captcha = "7Rp2k"

# beneficiary list for booking the slot. This can be fetched from the beneficiaries
beneficiaries = [
  # "28979499715650",
]

# In case, aware of the center for booking and waiting for the session to open
payload = json.dumps({
  "center_id": center_id,
  "session_id": session_id,
  "slot": slot_time,
  "captcha": captcha,
  "beneficiaries": beneficiaries,
  # update this to 2 if its for the second dose
  "dose": 1
})

with open("token.txt") as f:
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

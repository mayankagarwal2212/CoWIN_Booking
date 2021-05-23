#!/usr/bin/env python

import json
import http.client

url = "https://cdn-api.co-vin.in/api/v2/appointment/cancel"
conn = http.client.HTTPSConnection("cdn-api.co-vin.in")

# update the appointment id
appointment_id = "5b124e0a-245e-41e4-915c-89eb3e0f3eed"
# beneficiary list for booking the slot. This is the reference id of the user
beneficiaries = [
  # "28979499715650",
]

payload = json.dumps({
  "appointment_id": appointment_id,
  "beneficiariesToCancel": beneficiaries
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

conn.request("POST", "/api/v2/appointment/cancel", payload, headers)
resp = conn.getresponse()
data = resp.read()
response_data = json.loads(data)
print(response_data)

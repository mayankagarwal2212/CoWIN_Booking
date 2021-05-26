#!/usr/bin/env python

import hashlib, http.client, json, os, csv, sys
from sys import platform

from variables import *

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

def check_os():
  if platform == "linux" or platform == "linux2":
    return 1
  elif platform == "darwin":
    return 2
  elif platform == "win32":
    return 3

def get_python_version():
  return sys.version_info[0]

# -------------------------Generate OTP----------------------------

conn = http.client.HTTPSConnection("cdn-api.co-vin.in")
url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"

payload = json.dumps({
  "secret": "U2FsdGVkX18NuNa/jso3AJbIkh1Rf6DDBC58kOBELnGJA58OH/R5EKIz6hrONnCg2kTB8ktbqt0gyJ9aCKyWFw==",
  "mobile": COWIN_MOBILE_NUMBER,
})

headers = {
  'authority': 'cdn-api.co-vin.in',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://selfregistration.cowin.gov.in',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://selfregistration.cowin.gov.in/',
  'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
}

conn.request("POST", "/api/v2/auth/generateMobileOTP", payload, headers)

resp = conn.getresponse()
if resp.status != 200:
    print('Error Generate OTP: {} {}'.format(url, resp.status))
    raise Exception(resp)

data = resp.read()
response_data = json.loads(data)
print('Txn ID: {}'.format(response_data["txnId"]))
txnId = response_data["txnId"]

# # # -------------------------Verify OTP----------------------------

otp = input("Enter the otp: ")
otp = str(otp)

encoded_otp = encrypt_string(otp)
print(encoded_otp)

url = "https://cdn-api.co-vin.in/api/v2/auth/validateMobileOtp"

payload = json.dumps({
  "otp": encoded_otp,
  "txnId": txnId
})

headers = {
  'authority': 'cdn-api.co-vin.in',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'accept': 'application/json, text/plain, */*',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://selfregistration.cowin.gov.in',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://selfregistration.cowin.gov.in/',
  'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
}

conn.request("POST", "/api/v2/auth/validateMobileOtp", payload, headers)
resp = conn.getresponse()

if resp.status != 200:
    print('OTP Verification Failed: {} {}'.format(url, resp.status))
    raise Exception(resp)

data = resp.read()
response_data = json.loads(data)

token = response_data["token"]
print(token)

# -------------------------Add token ----------------------------------
file_name = "token.txt"
# for windows os, provide the absolute path
if check_os() == 3:
  file_name = '{}\\token.txt'.format(WINDOWS_ABSOLUTE_PATH)

f = open(file_name, "w")
f.write(token)
f.close()

# -------------------------Generate Captcha----------------------------

url = "https://cdn-api.co-vin.in/api/v2/auth/getRecaptcha"

payload = json.dumps({})
headers = {
  'authority': 'cdn-api.co-vin.in',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
  'accept': 'application/json, text/plain, */*',
  'authorization': 'Bearer {}'.format(token),
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'content-type': 'application/json',
  'origin': 'https://selfregistration.cowin.gov.in',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://selfregistration.cowin.gov.in/',
  'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
}

conn.request("POST", "/api/v2/auth/getRecaptcha", payload, headers)

resp = conn.getresponse()

if resp.status != 200:
    print('Cannot fetch captcha: {} {}'.format(url, resp.status))
    raise Exception(resp)

data = resp.read()
response_data = json.loads(data)

svg_xml = response_data['captcha']

file_name = "captcha.svg"
if check_os() == 3:
  file_name = '{}\\captcha.svg'.format(WINDOWS_ABSOLUTE_PATH)

f = open(file_name, "w")
f.write(svg_xml)
f.close()

# os.system("cairosvg captcha.svg -o captcha.png")
# os.remove("captcha.svg")

# -------------------------Read available slots--------------------

file_name = 'available_slots.csv'
if check_os() == 3:
  file_name = '{}\\available_slots.csv'.format(WINDOWS_ABSOLUTE_PATH)

available_slots = list(csv.DictReader(open(file_name, 'r')))
if len(available_slots) == 0:
  print("No slot available for booking")
  exit()

# -------------------------Book Slot----------------------------

print("Choose from the open slots\n")
session_id = None

for slot_info in available_slots:
  print(json.dumps(slot_info, indent=4))
  if (raw_input("Book this slot? - y/n\n").lower() if get_python_version() < 3 else input("Book this slot? - y/n\n").lower()) == 'y':
    session_id = slot_info.get('Session Id')
    center_id = slot_info.get('Center ID')
    slot = slot_info.get('Slot')
    break;

if session_id is None:
  print("No slot selected")
  exit()

captcha = raw_input("Enter the captcha :: \n") if get_python_version() < 3 else input("Enter the captcha :: \n")
request_data = {
  "center_id": int(center_id),
  "session_id": session_id,
  "slot": slot,
  "captcha": captcha,
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

#!/usr/bin/env python

import hashlib, requests, json, os

def encrypt_string(hash_string):
    sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature

# -------------------------Generate OTP----------------------------

url = "https://cdn-api.co-vin.in/api/v2/auth/generateMobileOTP"
# update the mobile number
mobile_number = 9999999999
payload = json.dumps({
  "secret": "U2FsdGVkX18NuNa/jso3AJbIkh1Rf6DDBC58kOBELnGJA58OH/R5EKIz6hrONnCg2kTB8ktbqt0gyJ9aCKyWFw==",
  "mobile": mobile_number
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

resp = requests.request("POST", url, headers=headers, data=payload)

if resp.status_code != 200:
    print('POST API: {} {}, Error message: {}'.format(url, resp.status_code, resp._content))
    raise Exception(resp)
else:
	print('Txn ID: {}'.format(resp.json()["txnId"]))
	txnId = resp.json()["txnId"]

# # # -------------------------Verify OTP----------------------------

print("Enter the otp")
otp = input()
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
  'content-Type': 'application/json',
  'origin': 'https://selfregistration.cowin.gov.in',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
  'sec-fetch-site': 'cross-site',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://selfregistration.cowin.gov.in/',
  'accept-language': 'en-IN,en;q=0.9,hi-IN;q=0.8,hi;q=0.7,en-GB;q=0.6,en-US;q=0.5'
}

response = requests.request("POST", url, headers=headers, data=payload)
# print(response.text)

if response.status_code != 200:
    print('POST API: {} {}, Error message: {}'.format(url, response.status_code, response._content))
    raise Exception(response)
else:
	token = response.json()["token"]
	print(token)

# -------------------------Add token ----------------------------------
f = open("token.txt", "w")
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

response = requests.request("POST", url, headers=headers, data=payload)

if response.status_code != 200:
  print("Exception raised :: {}".format(response._content))
  raise Exception(response)

svg_xml = json.loads(response._content)['captcha']

f = open("captcha.svg", "w")
f.write(svg_xml)
f.close()

os.system("cairosvg captcha.svg -o captcha.png")
os.remove("captcha.svg")

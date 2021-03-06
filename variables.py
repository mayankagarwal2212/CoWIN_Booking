
COWIN_MOBILE_NUMBER = 9999999999

# Search by PIN
PINCODE = '814112'

# To search by district, add district id here
DISTRICT_ID = ''

# age limit preference for alert
# for 45*, min_age_limit = 45
# for 18*, min_age_limit = 18
MIN_AGE_LIMIT = 18

# centers to exclude for alert, if any
CENTERS_TO_IGNORE = [
	# 701780,
	# 618194,
]

# add preferred centers to get alert for specific centers only
PREFERRED_CENTERS = [
	# 562896,
	# 609082,
]

# beneficiary list for booking the slot. This is the reference id of the user
BENEFICIARIES = [
	# 54764436180790,
]
# update this to 2 if its for the second dose
VACCINE_DOSE = 1

# update this with the vaccine eligible for 2nd dose
DOSE_2_VACCINE = 'COVAXIN'
DOSE_2_DUE_DATE = '11-06-2021'

###### Special window booking ########

# exclude centers to book slots directly in the special window
DIRECT_BOOKING_EXCLUDE_CENTERS = [
	# 676990,
]

# add preferred centers to book slots directly in the special window
DIRECT_BOOKING_PREFERRED_CENTERS = [
	# 562896,
]


# Update the appointment id to cancel a booking
BOOKED_APPOINTMENT_ID = ''

# Absolute path to this directory. For windows only
WINDOWS_ABSOLUTE_PATH = 'C:\\Users\\HP\\Documents\\CoWIN_Booking'


# Below settings are required only if you have configured twilio accoutn
# Reference: https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out.
SEND_WHATSAPP_ALERT = False
TWILIO_ACCOUNT_SID = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
TWILIO_AUTH_TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'

# this is the Twilio sandbox testing number
TWILIO_MOBILE_NUMBER = '+141XXXXXXXX'

# replace this number with your own WhatsApp Messaging number
TO_WHATSAPP_NUMBER = '+91810XXXXXX'

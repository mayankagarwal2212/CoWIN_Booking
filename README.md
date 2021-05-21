*********************************************************************************

***Requirements:***

python, pip

Python Dependencies:

twilio (pip install twilio)
requests (pip install requests)

**For Windows 10 user:**

win10toast (pip install win10toast)

Note: Make sure to start a fresh terminal

**For linux users:**

gnome-terminal

**For iOS users:**

Install iTerm, terminal-notifier

Make sure that the permission is configured. Allow full disk access permission to the following:

zsh, python, cron

Check this for more details: https://stackoverflow.com/questions/58844669/trying-to-run-a-python-script-with-cron-getting-errno-1-operation-not-permitt

Command to install terminal-notifier:
`gem install terminal-notifier`

*********************************************************************************

**How to configure:**

Download the `CoWIN_Booking` repository.

Configure twilio account to integrate whatsapp notification:

https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out

Update the scripts with the expected details, like the mobile number, pincode, preferred centers, min_age_limit, etc

Add the crontab to execute this every minute:

Open terminal

Enter the command `crontab -e`

This will open a file in the editor. Edit this and add the following:

`*/1 * * * * cd <path-to-this-directory> && /usr/bin/python cowin_alert.py >> <path-to-this-directory>/issues.txt 2>&1`

Here,

`/usr/bin/python` : This is the path to the directory for python. Update this based on the the configured path

Errors can be checked in the `issues.txt` file

*********************************************************************************

**How this works:**

This will create an alert as soon as the slot gets available for booking and checks for available slots every minute.
Once the slot is available, it will open the terminal for you.

Follow the steps shared on how to book the slot. Your slot will get booked.

*********************************************************************************

**How to book the slot:**

Generate the token and captcha required while booking the slot.
Run the following command:

`python generate_token.py`

When prompted, enter the otp received in the provided mobile number. This will generate a fresh token and the captcha.

Update the session_id, center_id, slot from the `available_slots.txt` file based on your preference. If you are aware of the center and waiting for the slot to open, you can update the script `generate_token.py` and generate the alert for this one only. One can merge the two scripts in this case.

Now, run `python book_slot.py`

Your slot will be booked.

Note: You can create an alias to execute these scripts for quick response

*********************************************************************************

**How to cancel my booking:**

Update the appointment_id in the `cancel_slot.py` and run the following command:

`python cancel_slot.py`

*********************************************************************************

References:

https://apisetu.gov.in/public/marketplace/api/cowin/

https://stackoverflow.com/questions/17651017/python-post-osx-notification

https://stackoverflow.com/questions/58844669/trying-to-run-a-python-script-with-cron-getting-errno-1-operation-not-permitt

https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out

https://towardsdatascience.com/how-to-make-windows-10-toast-notifications-with-python-fb3c27ae45b9


# Requirements

```
python, pip

Python Dependencies:

twilio (pip install twilio) => Only if you want to integrate whatsapp notification
```

**For Windows 10 user:**

win10toast (pip install win10toast)

Note: Make sure to start a fresh terminal

**For iOS users:**

Make sure that the permission is configured. Allow full disk access permission to the following:

zsh, python, cron

How to add permission: https://stackoverflow.com/questions/58844669/trying-to-run-a-python-script-with-cron-getting-errno-1-operation-not-permitt

# How to configure

Download the `CoWIN_Booking` repository.

Configure twilio account to integrate whatsapp notification:

https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out

Update the variables in the `variables.py` file with the expected details, like the mobile number, pincode, preferred centers, min_age_limit, etc

**For Windows user:**

Update the absolute path to this folder in `cowin_alert.bat` and `variables.py`.

Then,
```
Update the file `cowin_alert.bat` and update the python path and the path of `cowin_alert.py` file.
Now, add a new scheduler to run this every 5 minutes. To add this scheduler, execute the following steps:

Open Windows >> Task Scheduler
Create Task
In the general tab, add the task name. Click the checkbox "run with highest privileges".

In the Triggers tab >> Begin the task, select creation/update of this aciton.
Execute this task daily and repeat task every 5 minutes. (Or preferred interval)
Keep the trigger enabled.

In the actions tab, select action as "Start a program".
In the script path, add the cowin_alert.bat file.

Click on OK button and the scheduler is created
```

**For other users:**

```
Add the crontab to execute this every minute:
Open terminal
Enter the command `crontab -e`
This will open a file in the editor. Edit this and add the following:
`*/1 * * * * cd <path-to-this-directory> && /usr/bin/python cowin_alert.py >> <path-to-this-directory>/issues.txt 2>&1`

Here, `/usr/bin/python` : This is the path to the directory for python. Update this based on the the configured path

Errors can be checked in the `issues.txt` file
```

# How this works

This will create an alert as soon as the slot gets available for booking and checks for available slots every minute.
Once the slot is available, open a new terminal and follow the steps shared on how to book the slot. Your slot will get booked.

# How to book the slot

Generate the token required while booking the slot.
Run the following command:

`python book_appointment.py`

When prompted, enter the otp. This will generate a fresh token.

It will now prompt you to choose a slot from the available slots. Enter Y for the selected slot. Your slot will be booked.

Note: You can create an alias to execute these scripts for quick response

# Book slots in a special window

To book slots in a special window, when the slots are expected to be available, pre-generate the token.

First, execute the script: `python book_appointment.py`. Note that the token will expire in 15 mins, so execute this keeping in mind that the token does not expire during your slot availability window.

Execute the command `special_window_booking.py` in the special window.

# How to cancel my booking

Update the `BOOKED_APPOINTMENT_ID` in the `variables.py` file and execute the command: `python cancel_slot.py`

# References

https://apisetu.gov.in/public/marketplace/api/cowin/

https://stackoverflow.com/questions/17651017/python-post-osx-notification

https://stackoverflow.com/questions/58844669/trying-to-run-a-python-script-with-cron-getting-errno-1-operation-not-permitt

https://www.twilio.com/blog/send-whatsapp-message-30-seconds-python#:~:text=The%20above%20code%20imports%20the,sandbox%20to%20test%20it%20out

https://towardsdatascience.com/how-to-make-windows-10-toast-notifications-with-python-fb3c27ae45b9

https://stackoverflow.com/questions/23708898/pip-is-not-recognized-as-an-internal-or-external-command

https://www.winhelponline.com/blog/run-bat-files-invisibly-without-displaying-command-prompt/

**Do share your valuable feedback**

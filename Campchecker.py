import time

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import json

from urllib.request import urlopen

import datetime


# Sender and recipient details
smtp_server = "smtp.gmail.com"
smtp_port = 465
sender_email = "example@example.com" # Your gmail address
receiver_email = "example2@example2.com" # Email to send results to
app_password = "youremailpassword" # Your gmail password

# Create a multipart message
message = MIMEMultipart()
message["From"] = "Campsite Checker"
message["To"] = receiver_email
message["Subject"] = "Campsites are available!"

# locations to check
mapID =      ["-2147483610", "-2147483430"]
locationID = ["-2147483623", "-2147483543"]
campsite = ["Cultus Lake", "Rolley Lake"]

# Dates to check
date_strt = ["2023-09-01", "2023-09-08"]
date_end =  ["2023-09-03", "2023-09-11"]

# Time between searches (in seconds). I don't know how often we're allowed to check!
search_interval = 30

while True:
    for j in range(len(mapID)):
        for i in range(len(date_strt)):
                
            url = "https://camping.bcparks.ca/api/availability/map?mapId="+mapID[j]+"&bookingCategoryId=0&equipmentCategoryId=-32768&subEquipmentCategoryId=-32768&startDate="+date_strt[i]+"&endDate="+date_end[i]+"&getDailyAvailability=false&isReserving=true&filterData=%5B%5D&boatLength=null&boatDraft=null&boatWidth=null&partySize=1&numEquipment=null"

            try:
                # store the response of URL
                response = urlopen(url)

                # storing the JSON response 
                # from url in data
                data_json = json.loads(response.read())
            except:
                print("Error getting JSON")

            if data_json['mapAvailabilities'] == [0]:
                body = "Campsites have been found at "+campsite[j]+"\nFrom: "+date_strt[i]+" to: "+date_end[i]
                message.attach(MIMEText(body, "plain"))
                try:
                    # Create a secure SSL/TLS connection to the SMTP server
                    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                    server.ehlo()

                    # Login with the App Password
                    server.login(sender_email, app_password)

                    # Send the email
                    server.sendmail(sender_email, receiver_email, message.as_string())

                    print("Email sent successfully!")
                    del body
                    email_sent = 1
                except Exception as e:
                    print("An error occurred while sending the email:", str(e))
                    email_sent = 0
                finally:
                    # Close the SMTP server connection
                    server.quit()
            else:
                email_sent = 0

            # Break the inner for loop if email sent
            if(email_sent):
                break
            time.sleep(search_interval)
        # Break the outer for loop if email sent    
        if(email_sent):
            break
        else:
            ct = datetime.datetime.now()
            print("Nothing found ", ct)
    # Break while true                                                                                                                        
    if(email_sent):
            break

import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "rclarke009@gmail.com"
MY_PASSWORD = "YOUR PASSWORD"

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

while True:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.


    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    def send_email():
        file_path = f"letter.txt"
        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", "RECIPIENT")

        with smtplib.SMTP("YOUR EMAIL PROVIDER SMTP SERVER ADDRESS") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="RECIPIENTEMAIL",
                msg=f"Subject:Look up!\n\n{contents}"
            )

    #If the ISS is close to my current position
    # and it is currently dark
    # Then send me an email to tell me to look up.
    # BONUS: run the code every 60 seconds.

    """if my lat is equal to iss lat plus 5 or my lat is equal to iss lat minus 5 
    then check if it's dark OR
    if it's dark check( if time is earlier than sunrise but later than sunset) if my lat is equal to iss lat plus 5 or my lat is equal to iss lat minus 5 """

    #check every 30 seconds 
    if (time_now.hour < sunrise) or (time_now.hour > sunset):
        if (MY_LAT - 5 <= iss_latitude <= MY_LAT + 5):            send_email()
            print ("sent mail")

    time.sleep(30)  # Wait 30 seconds before next check


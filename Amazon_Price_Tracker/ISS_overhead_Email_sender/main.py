import smtplib
import time
import requests
import datetime as dt
from dotenv import dotenv_values

"""To create environment variable using .env.secret file and save the variables in it"""
config = {
    **dotenv_values("../.env.secret")
}

MY_LAT: float = float(config["MY_LAT"])
MY_LNG: float = float(config["MY_LNG"])

DAY_NIGHT_API = "https://api.sunrise-sunset.org/json"
ISS_API = "http://api.open-notify.org/iss-now.json"

EMAIL = config["MY_EMAIL"]
PASSWORD = config["MY_PASSWORD"]

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0

}


def iss_overhead():
    """Function checks ISS is overhead and returns True"""
    response = requests.get(url=ISS_API)
    response.raise_for_status()
    iss_json = response.json()

    iss_position = iss_json['iss_position']
    iss_position_lat = float(iss_position['latitude'])
    iss_position_lng = float(iss_position['longitude'])
    if (MY_LAT - 5 <= iss_position_lat < MY_LAT + 5) and (MY_LNG - 5 <= iss_position_lng <= MY_LNG + 5):
        return True


def checking_night():
    """Function checks the user location if it's night return True"""
    response = requests.get(url=DAY_NIGHT_API, params=parameters)
    response.raise_for_status()
    day_night_json = response.json()

    sunrise = int(day_night_json["results"]["sunrise"].split('T')[1].split(':')[0])
    sunset = int(day_night_json["results"]["sunset"].split('T')[1].split(':')[0])

    user_time_utc = dt.datetime.now(dt.timezone.utc).hour

    if (user_time_utc >= sunset) or (user_time_utc <= sunrise):
        return True


while True:
    """this loop will run every 60 seconds"""
    time.sleep(60)
    if checking_night() and iss_overhead():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,  # here to_address for which person want to send
                msg="Subject:From ISS :O\n\nLook up, The ISS is going overhead"
            )

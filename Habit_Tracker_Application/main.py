import requests.auth
from datetime import datetime
from dotenv import dotenv_values

config = {
    **dotenv_values("../.env.secret")
}

SHEETY_ENDPOINT = config["SHEETY_ENDPOINT"]
NUTRITIONIX_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

X_API_ID = config["API_ID"]
X_APP_KEY = config["APP_KEY"]

user = input("enter your activity: ".title())
nutrionix_params = {
    "query": user,
    "gender": "male",
    "weight_kg": 63,
    "height_cm": 180,
    "age": 22
}

nutrionix_headers = {
    "x-app-id": X_API_ID,
    "x-app-key": X_APP_KEY
}

response_with_nutritionix = requests.post(
    NUTRITIONIX_ENDPOINT,
    json=nutrionix_params,
    headers=nutrionix_headers)

result = response_with_nutritionix.json()

print("Nutritionix : ", result)

header = {
    "Authorization": config["AUTHORIZATION"]
}

date_in_string = datetime.now().strftime("%d/%m/%Y")
time_in_string = datetime.now().strftime("%X")
for workouts in result["exercises"]:
    working_time = str(workouts["duration_min"])
    SHEETY_data = {
        "workout": {
            "date": date_in_string,
            "time": time_in_string,
            "exercise": workouts["name"].title(),
            "duration": working_time,
            "calories": workouts["nf_calories"]
        }
    }
    response_with_sheety = requests.post(url=SHEETY_ENDPOINT,
                                         json=SHEETY_data,
                                         headers=header,
                                         auth=(
                                             config["SHEETY_USERNAME"],
                                             config["SHEETY_PASSWORD"]
                                         )
                                         )
    print("Sheety response : ",response_with_sheety.text)
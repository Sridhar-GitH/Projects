import requests.auth
from datetime import datetime
from dotenv import dotenv_values
import gspread
from oauth2client.service_account import ServiceAccountCredentials

config = {
    **dotenv_values("../.env.secret")
}

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    filename="../Credentials.json",
    scopes=SCOPE
)

client = gspread.authorize(CREDS)
sheets_tracker = client.open("My_Workouts").worksheet("workouts")

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
    headers=nutrionix_headers
)

result = response_with_nutritionix.json()

print("Nutritionix : ", result)

date_in_string = datetime.now().strftime("%d/%m/%Y")
time_in_string = datetime.now().strftime("%X")

for workouts in result["exercises"]:
    working_time = str(workouts["duration_min"])

    sheets_data = {
        "date": date_in_string,
        "time": time_in_string,
        "exercise": workouts["name"].title(),
        "duration": working_time,
        "calories": workouts["nf_calories"]
    }

    sheets_tracker.append_row(
        [
            sheets_data["date"],
            sheets_data["time"],
            sheets_data["exercise"],
            sheets_data["duration"],
            sheets_data["calories"],

        ]
    )

    print("Google Sheet : ", sheets_tracker)

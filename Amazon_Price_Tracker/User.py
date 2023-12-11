from bs4 import BeautifulSoup
import requests
import datetime as dt
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import dotenv_values

config = {
    **dotenv_values("../.env.secret")
}

SCOPE = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    filename="credentials.json",
    scopes=SCOPE
)

client = gspread.authorize(CREDS)
sheets_products = client.open("AmazonPriceTracker").worksheet("Products")
sheets_tracker = client.open("AmazonPriceTracker").worksheet("Tracker")

user_url = str(input("enter amazon product url: ".title()))
set_price = float(input("set the amount of the product to alert you : ₹".title()))

system_header = {
    "Accept-Language": config["ACCEPT_LANGUAGE"],
    "User-Agent": config["USER_AGENT"]
}


def finding():
    """functions checks the product tile and price and returns it"""
    response = requests.get(url=user_url, headers=system_header)
    soup = BeautifulSoup(response.content, "html.parser")
    find_title = soup.find("span", id="productTitle")
    find_price = soup.find("span", class_="a-price-whole")

    try:
        return find_title.get_text().strip(), find_price.get_text().strip(".").replace(",", "")
    except AttributeError:
        return None


finder = finding()

while finder is None:
    finder = finding()

title = finder[0]
price_as_float = float(finder[1])
today = dt.datetime.now().date()
today = today.strftime("%d-%m-%Y")

sheets_data = {
    "name_of_the_product": title,
    "price": price_as_float,
    "date": str(today),
    "set_amount": set_price,
    "product_url": user_url
}
sheets_products.append_row(
    [
        sheets_data["name_of_the_product"],
        sheets_data["price"],
        sheets_data["date"],
        sheets_data["set_amount"],
        sheets_data["product_url"]
     ]
)

sheets_tracker.append_row(
    [
        sheets_data["name_of_the_product"],
        sheets_data["price"],
        sheets_data["date"]
    ]
)

print("\nyour product added in the database successfully,\nit will remind you when the value it's down👍")
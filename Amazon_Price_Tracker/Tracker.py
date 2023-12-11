import pandas as pd
from bs4 import BeautifulSoup
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime as dt
import smtplib
from dotenv import dotenv_values

config = {
    **dotenv_values("../.env.secret")
}

EMAIL = config["MY_EMAIL"]
PASSWORD = config["MY_PASSWORD"]

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    filename="../Credentials.json",
    scopes=SCOPE
)
system_header = {
    "Accept-Language": config["ACCEPT_LANGUAGE"],
    "User-Agent": config["USER_AGENT"]
}

client = gspread.authorize(CREDS)
sheets_products = client.open("AmazonPriceTracker").worksheet("Products")
sheets_tracker = client.open("AmazonPriceTracker").worksheet("Tracker")

df = pd.DataFrame(sheets_products.get_all_records())
product_dict = df.to_dict()
unique_product = df["product_url"].unique()

today = dt.datetime.now().date()
today = today.strftime("%d-%m-%Y")


def tracking(product_url):
    """functions checks the product tile and price and returns it"""
    try:
        response = requests.get(url=product_url, headers=system_header)
        soup = BeautifulSoup(response.content, "html.parser")
        find_title = soup.find("span", id="productTitle")
        find_price = soup.find("span", class_="a-price-whole")

        return find_title.get_text().strip(), find_price.get_text().strip(".").replace(",", "")

    except AttributeError:
        return None


j = 0
for i in unique_product:
    if i == "":
        continue
    else:
        pass
    finder = tracking(product_url=i)
    while finder is None:
        finder = tracking(product_url=i)

    title = finder[0]
    current_price = int(finder[1])

    sheets_data = {
        "name_of_the_product": title,
        "price": current_price,
        "date": str(today),
    }

    sheets_tracker.append_row(
        [
            sheets_data["name_of_the_product"],
            sheets_data["price"],
            sheets_data["date"],
        ]
    )

    set_price = product_dict["set_amount"][j]
    j += 1

    if current_price <= set_price:
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,  # here to_address for which person want to send
                msg=f"Subject:From Amazon Tracker :O\n\nYour product {title} is now {set_price},"
                    f" Time is Counting, Don't Waste The Time To Buy it..."
            )

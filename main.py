import requests
import smtplib
import os
import datetime as dt
import html

MY_EMAIL = "___YOUR_EMAIL_HERE____"
MY_PASSWORD = "___YOUR_PASSWORD_HERE___"
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude
#API_KEY = os.environ['OWM_API_KEY']
API_KEY_ALPHAVANT = "VBVXA618VW7IJE2W"
API_KEY_NEWS = "b3948ae654f9401996d77a840b711ecb"
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def get_stock_price_diff():
    date_today = dt.date.today()
    date_yest = date_today - dt.timedelta(days=1)
    date_dby = date_today - dt.timedelta(days=2)

    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "interval": "5min",
        "apikey": API_KEY_ALPHAVANT,
    }

    response = requests.get("https://www.alphavantage.co/query", params=parameters)
    response.raise_for_status()
    stock_data = response.json()

    stock_price_y = float(stock_data["Time Series (Daily)"][f"{date_yest}"]["4. close"])
    stock_price_dby = float(stock_data["Time Series (Daily)"][f"{date_dby}"]["4. close"])

    stock_price_diff = stock_price_y-stock_price_dby
    stock_price_diff_perc = (stock_price_diff/stock_price_y)*100
    print(stock_price_y)
    print(stock_price_dby)
    print(round(stock_price_diff, 2))
    print(round(stock_price_diff_perc,2))
    if stock_price_diff_perc > 5:
        print("get news")
    else:
        print("no news")




## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news():

    parameters = {
        "qInTitle": COMPANY_NAME,
        "apiKey": API_KEY_NEWS,
    }

    response = requests.get("https://newsapi.org/v2/everything", params=parameters)
    response.raise_for_status()
    news_data = response.json()
    print(news_data)

    for n in range(0,3):
        print(html.unescape(news_data["articles"][n]["title"]))
        print(html.unescape(news_data["articles"][n]["description"]))



get_news()





## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


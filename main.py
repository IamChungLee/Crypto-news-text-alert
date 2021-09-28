import requests
from twilio.rest import Client
import os

SYMBOL = "ETH"
CRYPTO = "ethereum"


## STEP 1: Use https://www.alphavantage.co------------------------------------------------------------
# Calculate change in CRYPTO closing prices from daily closes obtained from alphavantage api
api_key = os.environ.get('VANTAGE_KEY')
alpha_endpoint = "https://www.alphavantage.co/query"

params = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": SYMBOL,
    "market": "USD",
    "apikey": api_key
}

#obtain json data from alphavantage.co API
response = requests.get(url=alpha_endpoint, params=params)
result = response.json()

                    #access time series here   #access the index of the lastes item    #get close
yesterday_close = float(result["Time Series (Digital Currency Daily)"][list(result["Time Series (Digital Currency Daily)"])[0]]['4a. close (USD)'])
day_before_yesterday_close = float(result["Time Series (Digital Currency Daily)"][list(result["Time Series (Digital Currency Daily)"])[1]]['4a. close (USD)'])


#Get the change in %
change_in_percent = (yesterday_close - day_before_yesterday_close)/day_before_yesterday_close * 100




## STEP 2: Use https://newsapi.org------------------------------------------------------------------------
#If price increase/decreases by 5% between yesterday and the day before yesterday get the first 3 news pieces for the CRYPTO.
news_api_key = os.environ.get('NEWS_KEY')
news_endpoint_url = "https://newsapi.org/v2/everything"

news_param = {
    "q": CRYPTO
}

header = {
    "X-Api-Key": news_api_key,
}

news_response = requests.get(url=news_endpoint_url, params=news_param, headers=header)
news_result = news_response.json()


headlines = []
briefs = []

#Grab the first 3 articles related to CRYPTO and append to lists
for i in range(3):
    headlines.append(list(news_result['articles'])[i]['title'])
    briefs.append(list(news_result['articles'])[i]['description'])


## STEP 3: Use https://www.twilio.com------------------------------------------------------------


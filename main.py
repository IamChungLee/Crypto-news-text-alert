import requests
from twilio.rest import Client
import os
import pandas
from flask import Flask, render_template, request

#FLASK-----------------------------------------------------------------#
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")


#This will check if the crypto symbol input by user exists
data = pandas.read_csv('digital_currency_list.csv')

#HOME----------------------------------------------------------------#
@app.route("/", methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        #SUBCRIBER INPUTS
        SYMBOL = request.form["symbol"].upper()
        PHONE_NUMBER = request.form["phone"]
        #goes through datafram to see if the symbol is there
        if data['symbol'].str.contains(SYMBOL).any():
            CRYPTO = data.loc[data["symbol"] == SYMBOL, "currency name"].values[0]
            print(CRYPTO)

            #Use https://www.alphavantage.co------------------------------------------------------------
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
            change_in_percent = abs(yesterday_close - day_before_yesterday_close)/day_before_yesterday_close * 100


            #Use https://newsapi.org------------------------------------------------------------------------
            #If price increase/decreases by 5% between yesterday and the day before yesterday get the first 3 news pieces for the CRYPTO.
            if change_in_percent >= 1:
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

            # Use https://www.twilio.com API to send alerts to subcriber------------------------------------------------------------

                account_sid = os.environ.get("TWILIO_SID")
                auth_token = os.environ.get("TWILIO_TOKEN")

                if yesterday_close > day_before_yesterday_close:
                    emoji = "????"
                else:
                    emoji = "????"

                #Text template used to send message to subscriber
                text_template = [f"ALERT!\n{CRYPTO}: {emoji} {change_in_percent}%\nHeadline: {headlines[n]}\nBrief: {briefs[n]}\n" for n in range(3)]
                print(text_template[0])

                #Use twilio api to send each headline and brief from text_template
                client = Client(account_sid, auth_token)
                for article in text_template:
                    message = client.messages \
                        .create(
                        body=article,
                        from_=os.environ.get("TWILIO_NUMBER"),
                        to=PHONE_NUMBER
                    )
                    print(message.status)
        else:
            print("Sorry but that currency does not exist please try another one.")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
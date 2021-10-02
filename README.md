# Crypto-news-text-alert
Hi This is a very simple yet efficient script that uses 3 APIs to send text alerts to the subcriber depending on the Crypto currency of their choice.
The alert will include the change in % and the top three news headlines relating to that currency.

To do that we first obtain three inputs which will be needed for each of the 3 APIs(I've already put three variables in place to use as an example):
1. The currency symbol (this will be used for the AlphaVantage API to grab the json data of the historical prices).
2. The name of the currency (this will be used in the NewsAPI to query the specific news we need).
   This will return us a json of all the top current news regarding that currency and then I grab the headline and description of the top 3 and put them in a list.
3. The phone number is used in the Twilio API to send a text alert directly to the inputed phone number.

This project is simple but it is used to demostrate what can be created with the use of APIs and utilizing them together.

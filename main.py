import requests
import datetime as dt
from twilio.rest import Client
SYMBOL = "BTC"
trend = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
account_sid = "AC38910b30f2e7be128f4530e82f57451c"
auth_token = "fe07ebe630005facf4e6ce8179bddb75"
parameters ={
    'function': "DIGITAL_CURRENCY_DAILY",
    'symbol': SYMBOL,
    'apikey': "SFHJM3OWEBUPT0IZ",
    'market': "USD"
}
today = dt.date.today()
r = requests.get(STOCK_ENDPOINT, params=parameters)
data = r.json()
price = [value for (key, value) in data['Time Series (Digital Currency Daily)'].items()]
yesterday_close_price = float(price[0]['4a. close (USD)'])
before_yesterday_price = float(price[1]['4a. close (USD)'])
remain = yesterday_close_price - before_yesterday_price
percentage_difference = abs(remain / before_yesterday_price * 100)

if remain > 0:
    trend = "△"
elif remain < 0:
    trend = "▼"
else:
    trend = "⧐"

    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
parameters2 = {
    'q': SYMBOL,
    'from': today,
    'apiKey': '73f138f170054875bcd8fc55f473fce6'
}

new_r = requests.get(NEWS_ENDPOINT, params=parameters2)
new_data = new_r.json()

news = new_data['articles'][:5]
articles = [f"Headline: {article['title']}\nDescription: {article['description']}."for article in news]
for article in articles:
    client = Client(account_sid, auth_token)
    message = client.messages \
            .create(
            body=f"{SYMBOL}: {trend}{round(percentage_difference, 2)}%\n{article}",
            from_='+14132986009',
            to='+18077098571'
    )

print(message.status)



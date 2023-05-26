import json
import smtplib
from email.message import EmailMessage
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os
from datetime import date
from datetime import timedelta

MESSAGING_TYPE = "sms"

load_dotenv()
STOCK = "OTLY"
COMPANY_NAME = "Oatly"
LIMIT = 2

# Get and format dates
TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)
DAY_BEFORE_YESTERDAY = TODAY - timedelta(days=2)

YESTERDAY = YESTERDAY.strftime("%Y-%m-%d")
DAY_BEFORE_YESTERDAY = DAY_BEFORE_YESTERDAY.strftime("%Y-%m-%d")


def get_daily_stock_prices():
    stock_key = os.environ.get("STOCK_KEY")
    url = 'https://www.alphavantage.co/query'
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": STOCK,
        "apikey": stock_key
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    return data["Time Series (Daily)"]


def calculate_difference(stock_prices: dict):
    yesterday_close = float(stock_prices[YESTERDAY]["4. close"])
    day_before_yesterday_close = float(stock_prices[DAY_BEFORE_YESTERDAY]["4. close"])

    difference_sum = yesterday_close - day_before_yesterday_close
    difference_percentage = (difference_sum / day_before_yesterday_close) * 100

    return round(difference_percentage)


def get_news_articles():
    url = "https://newsapi.org/v2/everything"
    news_key = os.environ.get("NEWS_KEY")
    params = {
        "q": COMPANY_NAME,
        "apiKey": news_key,
        "from": DAY_BEFORE_YESTERDAY,
        "to": YESTERDAY,
        "pageSize": 5,
        "sortBy": "relevancy"
    }
    response = requests.get(url, params)
    response.raise_for_status()
    data = response.json()
    return data["articles"]


def format_message(list_of_articles: list, percentage : int):
    if list_of_articles:
        formatted_articles = []
        for a in list_of_articles:
            a_url = f"Read article: {a['url']}"
            a_date = a['publishedAt'][:16].replace("T", " ")
            fa = f"Title: {a['title']}\nBrief: {a['description']}\nSource: {a['source']['name']}, {a_date}\n{a_url}"
            formatted_articles.append(fa)

        formatted_articles = "\n\n".join(formatted_articles)
        formatted_message = f"Good morning!\n\nHere is your alert to let you know that the closing price of stock {STOCK} changed more than {LIMIT}% between the day before yesterday and yesterday. Below are the {len(articles)} most relevant articles published between {DAY_BEFORE_YESTERDAY} and {YESTERDAY} that contain the keyword '{COMPANY_NAME}'. Perhaps they will give some hints to why the price changed!\n\n{formatted_articles}"
    else:
        formatted_message = f"No news articles found for {COMPANY_NAME} published in the past two days."

    if percentage < 0:
        formatted_percentage = str(percentage).replace('-', '🔻')
    else:
        formatted_percentage = f"🔺{str(percentage)}"
    formatted_header = f"{COMPANY_NAME} Closing Price Alert | {STOCK}: {formatted_percentage}%"

    return formatted_message, formatted_header


def send_email(message, header):
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_sender = os.environ.get("EMAIL_SENDER")
    email_recipient = os.environ.get("EMAIL_RECIPIENT")
    smtp_server = os.environ.get("SMTP_SERVER")
    port = os.environ.get("PORT")

    # Format email
    email = EmailMessage()
    email.set_content(message)
    #email.set_content(message, subtype='html')
    email["From"] = f"Your Stock Advisor<{email_sender}>"
    email["To"] = email_recipient
    email["Subject"] = header

    with smtplib.SMTP(host=smtp_server, port=port) as connection:
        connection.starttls()
        connection.login(user=email_sender, password=email_password)
        connection.send_message(email)
        connection.close()
        print(f"{TODAY} Email successfully sent to {email_recipient}!")


def send_sms(content):
    sms_account_sid = os.environ.get("SMS_ACCOUNT_SID")
    sms_token = os.environ.get("SMS_TOKEN")
    sms_sender = os.environ.get("SMS_SENDER")
    sms_recipient = os.environ.get("SMS_RECIPIENT")

    sms_content = f"\n\n{content}\nCheck your email for recent articles about {COMPANY_NAME}."

    client = Client(sms_account_sid, sms_token)
    client.messages.create(
        body=sms_content,
        from_=sms_sender,
        to=sms_recipient
    )
    print(f"{TODAY} SMS successfully sent to {sms_recipient}!")

# Run
stock_prices = get_daily_stock_prices()
percentage = calculate_difference(stock_prices)

if percentage > LIMIT or percentage < -LIMIT:

    articles = get_news_articles()
    full_message, brief_alert = format_message(articles, percentage)

    send_email(full_message, brief_alert)
    send_sms(brief_alert)


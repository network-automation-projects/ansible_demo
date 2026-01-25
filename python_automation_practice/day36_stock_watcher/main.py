import requests
from datetime import datetime, timedelta
from twilio.rest import Client
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

# ----------------------- CONFIGURATION ----------------------- #
STOCK = "TSLA"  # Change to your preferred stock symbol (e.g., AAPL for Apple)
COMPANY_NAME = "Tesla Inc"  # Full company name for news search

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_PHONE = os.getenv("TWILIO_FROM_PHONE")
MY_PHONE = os.getenv("MY_PHONE")

PERCENTAGE_THRESHOLD = 5  # Alert if change > 5%

# Alpha Vantage endpoint for daily stock data
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# ----------------------- GET STOCK DATA ----------------------- #
def get_stock_data():
    # #region agent log
    with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"B","location":"main.py:29","message":"Function entry - API key check","data":{"api_key_present":ALPHA_VANTAGE_API_KEY is not None,"api_key_length":len(ALPHA_VANTAGE_API_KEY) if ALPHA_VANTAGE_API_KEY else 0},"timestamp":int(datetime.now().timestamp()*1000)})+'\n')
    # #endregion
    parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=parameters)
    # #region agent log
    with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,E","location":"main.py:35","message":"Response received","data":{"status_code":response.status_code,"url":response.url},"timestamp":int(datetime.now().timestamp()*1000)})+'\n')
    # #endregion
    response.raise_for_status()
    data = response.json()
    # #region agent log
    with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,C,D","location":"main.py:37","message":"Response data keys","data":{"top_level_keys":list(data.keys()) if isinstance(data,dict) else "not_dict","has_error":any(k.lower() in ['error','note','information'] for k in (data.keys() if isinstance(data,dict) else []))},"timestamp":int(datetime.now().timestamp()*1000)})+'\n')
    # #endregion
    # #region agent log
    with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f:
        error_keys = [k for k in (data.keys() if isinstance(data,dict) else []) if k.lower() in ['error','note','information']]
        f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A,E","location":"main.py:38","message":"Error message check","data":{"error_keys":error_keys,"error_values":{k:data[k] for k in error_keys} if isinstance(data,dict) else {}},"timestamp":int(datetime.now().timestamp()*1000)})+'\n')
    # #endregion
    # #region agent log
    time_series_keys = [k for k in (data.keys() if isinstance(data,dict) else []) if 'time' in k.lower() and 'series' in k.lower()]
    with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f:
        f.write(json.dumps({"sessionId":"debug-session","runId":"post-fix","hypothesisId":"C,D","location":"main.py:59","message":"Time series key search","data":{"time_series_keys":time_series_keys,"expected_key":"Time Series (Daily)","has_expected":'Time Series (Daily)' in (data.keys() if isinstance(data,dict) else [])},"timestamp":int(datetime.now().timestamp()*1000)})+'\n')
    # #endregion

    # Check for API errors before accessing data
    if "Error Message" in data:
        raise ValueError(f"Alpha Vantage API Error: {data['Error Message']}")
    if "Information" in data:
        raise ValueError(f"Alpha Vantage API Error: {data['Information']}")
    if "Note" in data:
        raise ValueError(f"Alpha Vantage API Error: {data['Note']}")
    
    # Get the daily time series
    if "Time Series (Daily)" not in data:
        raise KeyError(f"Expected 'Time Series (Daily)' key not found in API response. Available keys: {list(data.keys())}")
    
    time_series = data["Time Series (Daily)"]
    dates = sorted(time_series.keys())[-2:]  # Last two trading days

    yesterday = time_series[dates[-1]]["4. close"]
    day_before = time_series[dates[-2]]["4. close"]

    yesterday_close = float(yesterday)
    day_before_close = float(day_before)

    difference = yesterday_close - day_before_close
    percentage_change = (difference / day_before_close) * 100

    up_down = "🔺" if difference > 0 else "🔻"

    return percentage_change, up_down, yesterday_close


# ----------------------- GET NEWS ----------------------- #
def get_news():
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    parameters = {
        "q": COMPANY_NAME,
        "from": yesterday_date,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_ENDPOINT, params=parameters)
    response.raise_for_status()
    articles = response.json()["articles"][:3]  # Top 3 articles

    return articles


# ----------------------- SEND SMS ----------------------- #
def send_sms(message):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=TWILIO_FROM_PHONE,
        to=MY_PHONE
    )
    print(message.status)


# ----------------------- MAIN LOGIC ----------------------- #
percentage_change, up_down, stock_price = get_stock_data()

if abs(percentage_change) >= PERCENTAGE_THRESHOLD:
    print(f"{STOCK}: {up_down}{abs(percentage_change):.2f}%")
    articles = get_news()

    for article in articles:
        headline = article["title"]
        brief = article["description"]
        msg = f"{STOCK}: {up_down}{abs(percentage_change):.2f}%\nHeadline: {headline}\nBrief: {brief}"
        send_sms(msg)
else:
    print(f"{STOCK} change ({percentage_change:.2f}%) below threshold. No alert sent.")
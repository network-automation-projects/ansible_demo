import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from err_handler import handle_api_errors

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

#stock key from https://www.alphavantage.co/support/#api-key is 2ZVP9AXDKRF79S4Y
#https://newsapi.org  https://newsapi.org/v2/everything?q=tesla&from=2025-12-07&sortBy=publishedAt&apiKey=41960454e95a40259ac9cf968dd160fb key is 41960454e95a40259ac9cf968dd160fb


load_dotenv()
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#get stock price for tesla at close today and at close yesterday
#compare, did it go up or down more than 5%, if yes
#print Get News

@handle_api_errors
def get_stock_price():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={ALPHAVANTAGE_API_KEY}'
    
    
    price = requests.get(url)
    data = price.json()

    # Check for API error messages
    if "Error Message" in data:
        print(f"API Error: {data['Error Message']}")
        return None
    
    if "Note" in data:
        print(f"API Note: {data['Note']}")  # Often indicates rate limiting
        return None
    

    time_series = data.get("Time Series (Daily)", {})

    if not time_series:
        print("No time series data available")
        return None

    #most recent 2 (today and yesterday)
    dates = sorted(time_series.keys(), reverse=True)[:2]

    if len(dates) >= 2:
        today_close = float(time_series[dates[0]]["4. close"])
        yesterday_close = float(time_series[dates[1]]["4. close"])
        
        print(f"Today's close: ${today_close}")
        print(f"Yesterday's close: ${yesterday_close}")
        
        # Calculate percentage change
        percent_change = ((today_close - yesterday_close) / yesterday_close) * 100
        
        print(percent_change)
        if percent_change > 5:
            get_news()

        return percent_change
    else:
        print("Not enough data available")
        return None

    


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
@handle_api_errors
def get_news():
    url = f'https://newsapi.org/v2/everything?q={"Tesla"}&from=2025-12-07&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}'
    
    news_feed = requests.get(url)
    
    news_data = news_feed.json()

    # Check for NewsAPI error messages (different format than Alpha Vantage)
    if news_data.get("status") == "error":
        print(f"NewsAPI Error: {news_data.get('message', 'Unknown error')}")
        return None
    
    if news_data.get("status") != "ok":
        print(f"Unexpected API status: {news_data.get('status', 'Unknown')}")
        return None

    articles = news_data.get("articles", [])[:3]  # Get first 3 articles

    if not articles:
        print("No articles found")
        return None

    for article in articles:
        print(f"Headline: {article.get('title', 'N/A')}")
        print(f"Brief: {article.get('description', 'N/A')}")
        print()  # Empty line between articles

    return articles  # Return articles for potential use in Step 3
    



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

def send_SMS():




get_stock_price()

get_news() #for testing

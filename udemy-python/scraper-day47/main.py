import requests
from bs4 import BeautifulSoup
import smtplib
import os

MY_EMAIL = os.getenv("MY_EMAIL", "YOUR EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD", "YOUR PASSWORD")

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # Default to Gmail
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  # Default TLS port

live_url = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"

# Full headers would look something like this
header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
    "Dnt": "1",
    "Priority": "u=1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
}

def get_price(url) -> tuple[float, BeautifulSoup]:
    try:
        response = requests.get("https://appbrewery.github.io/instant_pot/", headers=header)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        webpage = response.text
        soup = BeautifulSoup(webpage, "html.parser")
        
        prices = soup.find_all(class_="a-offscreen")
        
        if not prices:
            print("No prices found on the page")
        else:
            for price in prices:
                price_text = price.get_text().strip()
                # Remove commas and other non-numeric characters except decimal point
                price_text = price_text.replace(",", "").replace("$", "").strip()
                
                try:
                    price_value = float(price_text)
                    print(price_value)
                    return price_value, soup
                except ValueError:
                    print(f"Could not convert '{price_text}' to float")
                    
    except requests.exceptions.RequestException as e:
        print(f"Network/Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None, None

def send_email(price: float, soup: BeautifulSoup, url: str):
    """Send email alert when price drops below threshold."""
    if soup is None:
        print("Cannot send email: soup object is None")
        return
        
    try:
        item_name_elem = soup.find(class_="a-size-medium a-color-base a-text-normal")
        item_link_elem = soup.find(class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
        
        item_name = item_name_elem.get_text().strip() if item_name_elem else "Item"
        item_link = item_link_elem.get("href") if item_link_elem else url
        if item_link and not item_link.startswith("http"):
            item_link = f"https://www.amazon.com{item_link}"
        
        contents = f"The {item_name}: {item_link} has a lower price!   ${price:.2f}"
        
        # Check if credentials are set
        if MY_EMAIL == "YOUR EMAIL" or MY_PASSWORD == "YOUR PASSWORD":
            print("Email credentials not configured. Set MY_EMAIL and MY_PASSWORD environment variables.")
            print(f"Would send email with contents: {contents}")
            return
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,  # Send to self, or set TO_EMAIL env var
                msg=f"Subject:Price Alert!\n\n{contents}"
            )
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")

def main():
    price, soup = get_price(live_url)
    if price is not None and price < 100:
        send_email(price, soup, live_url)   

if __name__ == "__main__":
    main()
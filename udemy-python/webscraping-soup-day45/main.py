import requests
from bs4 import BeautifulSoup

#what i learned from this is that parsing by hand is a pain in the butt.

response = requests.get("https://news.ycombinator.com")
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")

article_texts = []
article_links = []
article_upvotes = []

# Find all score elements first
scores = soup.find_all("span", class_="score")

print(f"Found {len(scores)} scores")

for score in scores:
    try:
        upvote_count = int(score.get_text().split()[0])
        
        # Find the parent table row
        score_row = score.find_parent("tr")
        if score_row:
            # Go up to find the previous sibling row (the article row)
            article_row = score_row.find_previous_sibling("tr", class_="athing")
            if article_row:
                # Find the titleline span, then get the link inside it
                titleline_span = article_row.find("span", class_="titleline")
                if titleline_span:
                    article_tag = titleline_span.find("a")
                else:
                    # Fallback: try finding link directly
                    article_tag = article_row.find("a", class_="storylink") or article_row.find("a", href=True)
                
                if article_tag:
                    article_text = article_tag.get_text().strip()
                    article_link = article_tag.get("href")
                    
                    # Make sure it's a full URL (Hacker News uses relative URLs for internal links)
                    if article_link and not article_link.startswith("http"):
                        article_link = "https://news.ycombinator.com" + article_link if article_link.startswith("/") else f"https://news.ycombinator.com/{article_link}"
                    
                    # Only add if we got actual text
                    if article_text:
                        article_texts.append(article_text)
                        article_links.append(article_link)
                        article_upvotes.append(upvote_count)
    except (ValueError, AttributeError) as e:
        # Skip if we can't parse the score or find the article
        continue

print(f"Found {len(article_upvotes)} articles with upvotes")

# Check if we found any articles before trying to get max
if article_upvotes:
    #get the article with the most upvotes
    top_upvotes = max(article_upvotes)
    top_article_index = article_upvotes.index(top_upvotes)
    top_article_text = article_texts[top_article_index] 
    top_article_link = article_links[top_article_index]

    print(f"Highest upvotes: {top_upvotes}")
    print(f"Top Article: {top_article_text}")
    print(f"Link: {top_article_link}")
else:
    print("No articles with upvotes found")
    # Debug: let's see what we found
    print(f"Found {len(scores)} scores")
    article_rows = soup.find_all("tr", class_="athing")
    print(f"Found {len(article_rows)} article rows")
# response = requests.get("https://news.ycombinator.com")
# web_page = response.text

# soup = BeautifulSoup(web_page, "html.parser")
# articles = soup.find_all("a", class_="storylink")

# article_texts = []
# article_links = []
# article_upvotes = []

# scores = soup.find_all("span", class_="score")

# for score in scores:
#     # Get the upvote count
#     upvote_count = int(score.get_text().split()[0])
    
#     # Find the parent row (usually a <tr> or container with class "athing")
#     parent_row = score.find_parent("tr")
#     if parent_row:
#         # Find the article link within this parent row
#         article_tag = parent_row.find("a", class_="storylink")
#         if article_tag:
#             article_text = article_tag.get_text()
#             article_link = article_tag.get("href")
            
#             # Only add if we found both article and upvote
#             article_texts.append(article_text)
#             article_links.append(article_link)
#             article_upvotes.append(upvote_count)

# #get the article with the most upvotes
# top_upvotes = max(article_upvotes)
# top_article_index = article_upvotes.index(top_upvotes)
# top_article_text = article_texts[top_article_index] 
# top_article_link = article_links[top_article_index]

# print(f"Highest upvotes: {top_upvotes}")
# print(f"Top Article: {top_article_text}")
# print(f"Link: {top_article_link}")


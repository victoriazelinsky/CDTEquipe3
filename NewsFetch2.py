
import requests
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# load API key 
API_KEY = "c97bc348b78840749d2c45aae7cc5290"

# dates for the last X days
to_date = datetime.utcnow().date()
from_date = to_date - timedelta(days=7)

QUERY = 'India Pakistan war OR conflict OR border OR attack OR tension'
LANG = 'en'
PAGE_SIZE = 5  # max per page

def fetch_news(query, from_date, to_date, api_key, page_size=100):
    url = 'https://newsapi.org/v2/everything'
    all_articles = []
    for page in range(1, 3):  # try up to 5 pages
        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'language': LANG,
            'pageSize': page_size,
            'page': page,
            'sortBy': 'publishedAt',
            'apiKey': api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print("Error:", data.get("message"))
            break

        articles = data.get("articles", [])
        if not articles:
            break
        all_articles.extend(articles)
    return all_articles

# fetch articles
articles = fetch_news(QUERY, from_date.isoformat(), to_date.isoformat(), API_KEY)

# convert to dataframe
df = pd.DataFrame([{
    'title': article['title'],
    'description': article['description'],
    'source': article['source']['name'],
    'published_at': article['publishedAt'],
    'url': article['url'],
    'content': article['content']
} for article in articles])

# save to CSV
df.to_csv("india_pakistan_conflict_news.csv", index=False)
print(f"{len(df)} articles saved to 'india_pakistan_conflict_news.csv'")
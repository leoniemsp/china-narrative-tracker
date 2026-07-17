from newsapi import NewsApiClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

api_key = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=api_key)

articles = newsapi.get_everything(
    q="China",
    language="en",
    sort_by="publishedAt",
    page_size=1
)

article = articles["articles"][0]
print("\nTITLE:")
print(article["title"])

print("\nAUTHOR:")
print(article["author"])

print("\nSOURCE:")
print(article["source"]["name"])

print("\nDATE:")
print(article["publishedAt"])

print("\nDESCRIPTION:")
print(article["description"])

print("\nURL:")
print(article["url"])

print("\nCONTENT:")
print(article["content"])
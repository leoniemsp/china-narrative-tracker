from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import pandas as pd

load_dotenv(dotenv_path=".env")

api_key = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=api_key)

articles = newsapi.get_everything(
    q="China",
    language="en",
    sort_by="publishedAt",
    page_size=100
)

data = []
for article in articles["articles"]:
     
    score = 0

    title = article["title"] or " "
    content = article["content"] or " "

    keywords = [
        "China",
        "Chinese",
        "Xi",
        "Beijing",
        "Shanghai",
        "Hong Kong"
    ]

    for keyword in keywords:

        if keyword in article["title"]:
            score += 2

        if keyword in article["content"]:
            score += 1

    data.append({
            "title": article["title"],
            "author": article["author"],
            "source": article["source"],
            "publishedAt": article["publishedAt"],
            "description": article["description"],
            "url": article["url"],
            "content": content,
            "china_score": score
        })

df = pd.DataFrame(data)

china_articles = df[df["china_score"] > 0]
print(china_articles[["title", "china_score"]])

china_articles.to_csv("china_articles.csv", index=False)
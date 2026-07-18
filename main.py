#Imports
from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import pandas as pd

load_dotenv(dotenv_path=".env")

#API Key
api_key = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=api_key)

articles = newsapi.get_everything(
    q="China",
    language="en",
    sort_by="publishedAt",
    page_size=100
)

data = []

#Define functions
def calculate_china_score(title, content):

    score = 0

    keywords = [
        "China",
        "Chinese",
        "Xi",
        "Beijing",
        "Shanghai",
        "Hong Kong"
    ]

    for keyword in keywords:

        if keyword.lower() in title.lower():
            score += 2

        if keyword.lower() in content.lower():
            score += 1

    return score

def classify_topics(full_text):

    topics = []

    Tech_keywords = [
        "AI",
        "DeepSeek",
        "semiconductor",
        "robotics",
        "EV",
        "battery",
        "Huawei",
        "BYD"
    ]

    Economy_keywords = [
        "GDP",
        "trade",
        "economy",
        "tariffs",
        "exports",
        "imports"
    ]
    
    Business_keywords = [
        "IPO",
        "earnings",
        "investment",
        "company",
        "startup"
    ]

    Geopolitics_keywords = [
        "summit",
        "minister",
        "relations",
        "cooperation",
        "agreement",
        "sanctions"
    ]

    if any(keyword.lower() in full_text.lower() for keyword in Tech_keywords):
        topics.append("Tech")

    if any(keyword.lower() in full_text.lower() for keyword in Economy_keywords):
        topics.append("Economy")

    if any(keyword.lower() in full_text.lower() for keyword in Business_keywords):
        topics.append("Business")

    if any(keyword.lower() in full_text.lower() for keyword in Geopolitics_keywords):
        topics.append("Geopolitics")

    if len(topics) == 0:
        topics.append("Other")

    return topics

#Anayliyze articles
for article in articles["articles"]:

    title = article["title"] or ""
    content = article["content"] or ""

    full_text = title + " " + content

    score = calculate_china_score(title, content)

    topics = classify_topics(full_text)

#Build DataFrame
    data.append({
            "title": article["title"],
            "author": article["author"],
            "source": article["source"]["name"],
            "publishedAt": article["publishedAt"],
            "description": article["description"],
            "url": article["url"],
            "content": content,
            "china_score": score,
            "topic": ", ".join(topics)
        })

df = pd.DataFrame(data)

#Show results
china_articles = df[df["china_score"] > 0]

print("\nNumber of China articles:")
print(len(china_articles))

print("\nSources:")
print(china_articles["source"].value_counts())

china_articles = df[df["china_score"] > 0]
print(china_articles[["title", "topic", "china_score"]])

print("\nTopics:")
print(china_articles["topic"].value_counts())

print("\nAverage China Score:")
print(china_articles["china_score"].mean())

#Save to CSV
china_articles.to_csv("china_articles.csv", index=False)
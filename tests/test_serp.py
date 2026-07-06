from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("SERP_API_KEY"))
params = {
    "engine": "google",
    "q": "Best attractions in Tokyo",
    "api_key": os.getenv("SERP_API_KEY")
}

search = GoogleSearch(params)

results = search.get_dict()

print(results)
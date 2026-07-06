from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()


def search_hotels(
    destination: str,
    check_in: str,
    check_out: str):
    params = {
    "engine": "google_hotels",
    "q": destination,
    "check_in_date": check_in,
    "check_out_date": check_out,
    "currency": "EUR",
    "gl": "de",
    "hl": "en",
    "api_key": os.getenv("SERP_API_KEY")
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    hotels = []

    for hotel in results.get(
        "properties",
        []
    )[:5]:

        try:

            price_per_night = hotel[
                "rate_per_night"
            ][
                "extracted_lowest"
            ]
            total_price = hotel[
                "total_rate"
            ][
                "extracted_lowest"
            ]

            hotels.append(
                {
                    "name":
                        hotel["name"],

                    "price_per_night":
                        price_per_night,

                    "total_price":
                        total_price,

                    "rating":
                        hotel.get(
                            "overall_rating",
                            0
                        ),

                    "amenities":
                        hotel.get(
                            "amenities",
                            []
                        )[:5]
                }
            )

        except Exception:
            continue

    return hotels
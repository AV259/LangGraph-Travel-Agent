import pandas as pd

airports_df = pd.read_csv(
    "C:\\Users\\Akash Verma\\TravelMind_AI\\data\\airports.csv"
)

# Keeping only airports with IATA codes
airports_df = airports_df[
    airports_df["iata_code"].notna()
]

def get_iata_code(city_name: str):

    matches = airports_df[
        airports_df["municipality"]
        .str.lower()
        .str.contains(
            city_name.lower(),
            na=False
        )
    ]

    if len(matches) == 0:
        return None

    return matches.iloc[0]["iata_code"]
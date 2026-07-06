# Sample itinerary data structure
sample_itinerary = {
    "trip_summary": "A 7-day cultural and historical immersion in Rajasthan, India, from October 5th to October 12th, 2026, focusing on Jaipur, Ranthambore, and Jodhpur.",
    "flight_summary": "Round trip flight with Etihad, departing October 5th at 22:30 and arriving October 6th at 19:35 in Jaipur.",
    "hotel_summary": "Rajasthan Palace - A Heritage Boutique Hotel in Jaipur, €47/night for €327 total.",
    "budget_summary": "Total cost €1195, leaving €2805 remaining. Trip is well within budget.",
    "travel_tips": [
        "Dress modestly when visiting religious sites",
        "Stay hydrated with bottled water",
        "Bargaining is common in local markets",
        "Keep small currency denominations handy"
    ],
    "days": [
        {
            "day": 1,
            "morning": "Depart from Munich on October 5th.",
            "afternoon": "Continue your journey to India.",
            "evening": "Arrive at Jaipur International Airport (JAI) at 19:35. Transfer to hotel and check-in."
        },
        {
            "day": 2,
            "morning": "Visit the iconic Hawa Mahal (Palace of Winds) and City Palace.",
            "afternoon": "Journey to the magnificent Amber Fort.",
            "evening": "Immerse yourself in Rajasthani culture at Chokhi Dhani."
        }
    ]
}

sample_flight = {
    'airline': 'Etihad',
    'departure_time': '2026-10-05 22:30',
    'arrival_time': '2026-10-06 19:35',
    'price': 581,
    'total_duration': 1055
}

sample_hotel = {
    'name': 'Rajasthan Palace - A Heritage Boutique Hotel in Jaipur',
    'price_per_night': 47,
    'total_price': 327,
    'rating': 4.6,
    'amenities': ['Breakfast ($)', 'Free Wi-Fi', 'Free parking', 'Outdoor pool']
}

sample_budget = {
    'total_cost': 1195,
    'remaining_budget': 2805.0,
    'budget_status': 'within_budget'
}

# Display the formatted output
output = []

output.append("=" * 70)
output.append("YOUR PERSONALIZED TRAVEL ITINERARY".center(70))
output.append("=" * 70)
output.append("")

output.append(" TRIP SUMMARY")
output.append("-" * 70)
output.append(sample_itinerary["trip_summary"])
output.append("")

output.append("  FLIGHT DETAILS")
output.append("-" * 70)
output.append(f"Airline: {sample_flight['airline']}")
output.append(f"Departure: {sample_flight['departure_time']}")
output.append(f"Arrival: {sample_flight['arrival_time']}")
output.append(f"Duration: {sample_flight['total_duration']} minutes")
output.append(f"Cost: €{sample_flight['price']}")
output.append("")

output.append(" PRIMARY ACCOMMODATION")
output.append("-" * 70)
output.append(f"Hotel: {sample_hotel['name']}")
output.append(f"Rating:  {sample_hotel['rating']}")
output.append(f"Price per Night: €{sample_hotel['price_per_night']}")
output.append(f"Total: €{sample_hotel['total_price']}")
output.append(f"Amenities: {', '.join(sample_hotel['amenities'])}")
output.append("")

output.append(" BUDGET SUMMARY")
output.append("-" * 70)
output.append(f"Total Cost: €{sample_budget['total_cost']}")
output.append(f"Remaining Budget: €{sample_budget['remaining_budget']}")
output.append(f"Status: {sample_budget['budget_status'].upper()}")
output.append("")

output.append(" TRAVEL TIPS")
output.append("-" * 70)
for idx, tip in enumerate(sample_itinerary['travel_tips'], 1):
    output.append(f"{idx}. {tip}")
output.append("")

output.append(" DAY-BY-DAY ITINERARY")
output.append("=" * 70)
output.append("")

for day in sample_itinerary['days']:
    output.append(f"DAY {day['day']}: October {4 + day['day']}, 2026")
    output.append("-" * 70)
    output.append(" Morning:")
    output.append(f"   {day['morning']}")
    output.append("")
    output.append(" Afternoon:")
    output.append(f"   {day['afternoon']}")
    output.append("")
    output.append(" Evening:")
    output.append(f"   {day['evening']}")
    output.append("")
    output.append("")

output.append("=" * 70)
output.append("Have a wonderful trip! Safe travels! ".center(70))
output.append("=" * 70)

print("\n".join(output))

from app.tools.hotel_tool import (
    search_hotels
)

hotels = search_hotels(
    destination="Delhi",
    check_in="2026-07-16",
    check_out="2026-07-21"
)

print(hotels)
from app.state.travel_state import TravelState


REQUIRED_FIELDS = [
    "destination",
    "departure_city",
    "start_date",
    "end_date",
    "duration",
    "budget"
]


def get_missing_fields(state: TravelState):

    missing_fields = []

    for field in REQUIRED_FIELDS:

        value = state.get(field)

        if value is None:
            missing_fields.append(field)

    return missing_fields
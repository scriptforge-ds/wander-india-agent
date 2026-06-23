# Average daily per-person costs in ₹ for budget travelers

BUDGET_DEFAULTS = {
    "north_hills": {
        "stay": 400,        # dorm / guesthouse
        "food": 250,        # dhabas, local meals
        "local_transport": 100,
        "misc": 100,
        "total_per_day": 850,
    },
    "south": {
        "stay": 500,
        "food": 200,
        "local_transport": 80,
        "misc": 100,
        "total_per_day": 880,
    },
    "beach": {
        "stay": 500,
        "food": 250,
        "local_transport": 80,
        "misc": 120,
        "total_per_day": 950,
    },
    "high_altitude": {
        "stay": 600,        # limited options, costlier
        "food": 300,
        "local_transport": 200,
        "misc": 150,
        "total_per_day": 1250,
    },
    "northeast": {
        "stay": 350,
        "food": 200,
        "local_transport": 100,
        "misc": 100,
        "total_per_day": 750,
    },
    "plains_heritage": {
        "stay": 400,
        "food": 150,
        "local_transport": 80,
        "misc": 100,
        "total_per_day": 730,
    },
}

# Region mapping for destinations
DESTINATION_REGION_MAP = {
    "kedarkantha": "north_hills",
    "chopta": "north_hills",
    "valley_of_flowers": "north_hills",
    "spiti": "high_altitude",
    "ladakh": "high_altitude",
    "coorg": "south",
    "chikmagalur": "south",
    "hampi": "plains_heritage",
    "gokarna": "beach",
    "majuli": "northeast",
}


def get_daily_budget(destination_key: str) -> dict:
    """
    Returns budget breakdown for a destination.
    """
    region = DESTINATION_REGION_MAP.get(destination_key, "south")
    budget = BUDGET_DEFAULTS.get(region, BUDGET_DEFAULTS["south"])
    return {"destination": destination_key, "region": region, **budget}


def estimate_trip_cost(destination_key: str, days: int, people: int) -> dict:
    """
    Returns total estimated trip cost.
    """
    daily = get_daily_budget(destination_key)
    total = daily["total_per_day"] * days * people
    return {
        "days": days,
        "people": people,
        "daily_per_person": daily["total_per_day"],
        "total_estimate": total,
        "breakdown": {
            "stay": daily["stay"] * days * people,
            "food": daily["food"] * days * people,
            "local_transport": daily["local_transport"] * days * people,
            "misc": daily["misc"] * days * people,
        }
    }
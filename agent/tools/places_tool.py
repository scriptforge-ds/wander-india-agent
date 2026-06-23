from data.destinations import DESTINATIONS


def search_destinations(
    trip_type: str = None,
    month: int = None,
    max_daily_budget: int = None,
    region: str = None,
    tags: list[str] = None,
    difficulty: str = None,
) -> list:
    """
    Filters destinations based on user preferences.
    Returns a ranked list of matching destinations.
    """
    results = []

    for key, dest in DESTINATIONS.items():
        # Filter by trip type
        if trip_type and trip_type not in dest["type"]:
            continue

        # Filter by month (must be in best_months, not in avoid_months)
        if month:
            if month in dest.get("avoid_months", []):
                continue
            if month not in dest.get("best_months", []):
                continue

        # Filter by budget
        if max_daily_budget and dest["avg_daily_cost"] > max_daily_budget:
            continue

        # Filter by region
        if region and dest.get("region") != region:
            continue

        # Filter by difficulty
        if difficulty and dest.get("difficulty") != difficulty:
            continue

        # Filter by tags (at least one tag must match)
        if tags:
            dest_tags = dest.get("tags", [])
            if not any(t.lower() in dest_tags for t in tags):
                continue

        results.append({"key": key, **dest})

    # Sort by avg_daily_cost (cheapest first)
    results.sort(key=lambda x: x["avg_daily_cost"])
    return results


def get_destination_detail(destination_key: str) -> dict:
    """
    Returns full details for a single destination.
    """
    dest = DESTINATIONS.get(destination_key)
    if not dest:
        return {"error": f"Destination '{destination_key}' not found"}
    return {"key": destination_key, **dest}


def get_all_keys() -> list:
    return list(DESTINATIONS.keys())
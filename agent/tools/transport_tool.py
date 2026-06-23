from data.transport_routes import get_route


def get_transport_options(origin: str, destination: str) -> dict:
    """
    Returns all transport options between two cities with cost + duration.
    """
    route = get_route(origin, destination)

    if "error" in route:
        return {
            "status": "no_data",
            "message": route["error"],
            "fallback": _generic_advice(origin, destination)
        }

    options = []
    for mode, details in route.items():
        options.append({
            "mode": mode,
            "cost_inr": details.get("cost"),
            "duration_hrs": details.get("duration"),
            "operator": details.get("operator") or details.get("train") or "—",
            "note": details.get("note", "")
        })

    # Sort by cost
    options.sort(key=lambda x: x["cost_inr"] or 9999)

    return {
        "status": "ok",
        "origin": origin,
        "destination": destination,
        "options": options,
        "budget_pick": options[0] if options else None
    }


def estimate_transport_cost_for_trip(
    origin: str,
    destination: str,
    people: int,
    prefer_mode: str = "bus"
) -> dict:
    """
    Estimates total transport cost for a group.
    """
    route_data = get_transport_options(origin, destination)

    if route_data["status"] == "no_data":
        return route_data

    options = route_data["options"]
    preferred = next((o for o in options if prefer_mode in o["mode"]), options[0])

    one_way = preferred["cost_inr"] * people
    return {
        "mode": preferred["mode"],
        "cost_per_person": preferred["cost_inr"],
        "people": people,
        "one_way_total": one_way,
        "return_total": one_way * 2,
        "duration_hrs": preferred["duration_hrs"],
        "operator": preferred["operator"],
    }


def _generic_advice(origin: str, destination: str) -> str:
    return (
        f"No direct route data found for {origin} → {destination}. "
        f"Check redbus.in or railyatri.in for buses, "
        f"and irctc.co.in for trains."
    )
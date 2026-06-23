from data.budget_defaults import get_daily_budget, estimate_trip_cost
from data.transport_routes import get_route


def calculate_full_trip_budget(
    destination_key: str,
    days: int,
    people: int,
    origin: str = None,
    include_transport: bool = True
) -> dict:
    """
    Calculates complete trip budget including travel cost.
    """
    # Daily costs at destination
    trip = estimate_trip_cost(destination_key, days, people)

    result = {
        "destination": destination_key,
        "days": days,
        "people": people,
        "daily_per_person": trip["daily_per_person"],
        "stay_total": trip["breakdown"]["stay"],
        "food_total": trip["breakdown"]["food"],
        "local_transport_total": trip["breakdown"]["local_transport"],
        "misc_total": trip["breakdown"]["misc"],
        "at_destination_total": trip["total_estimate"],
        "travel_cost": 0,
        "grand_total": trip["total_estimate"],
    }

    # Add travel cost if origin provided
    if origin and include_transport:
        route = get_route(origin, destination_key)
        if "error" not in route:
            cheapest_mode = min(route.items(), key=lambda x: x[1].get("cost", 9999))
            travel_cost = cheapest_mode[1]["cost"] * people * 2  # return trip
            result["travel_cost"] = travel_cost
            result["travel_mode"] = cheapest_mode[0]
            result["grand_total"] += travel_cost

    return result


def check_budget_feasibility(
    total_budget: int,
    destination_key: str,
    days: int,
    people: int,
    origin: str = None
) -> dict:
    """
    Checks if a user's budget is feasible for a trip.
    Returns verdict + suggestions if tight.
    """
    budget_calc = calculate_full_trip_budget(
        destination_key, days, people, origin
    )
    estimated = budget_calc["grand_total"]
    difference = total_budget - estimated

    if difference >= 0:
        verdict = "✅ Budget is sufficient"
        suggestion = f"You'll have ₹{difference:,} to spare."
    elif difference >= -1000:
        verdict = "⚠️ Budget is tight"
        suggestion = "Cut 1-2 days or reduce group size to fit."
    else:
        verdict = "❌ Budget is insufficient"
        suggestion = (
            f"You're short by ₹{abs(difference):,}. "
            f"Consider fewer days, nearby cheaper destination, "
            f"or travel in offseason for lower prices."
        )

    return {
        "user_budget": total_budget,
        "estimated_cost": estimated,
        "difference": difference,
        "verdict": verdict,
        "suggestion": suggestion,
        "breakdown": budget_calc,
    }
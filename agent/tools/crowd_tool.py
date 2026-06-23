from data.peak_seasons import get_crowd_level, CROWD_LABELS

def get_crowd_info(destination_key: str, month: int) -> dict:
    """
    Returns crowd level, label, and travel recommendation.
    """
    info = get_crowd_level(destination_key, month)

    level = info.get("level")

    if level == 0:
        recommendation = "Do not travel — destination is closed or inaccessible this month."
    elif level == 1:
        recommendation = "Great time to visit — very few tourists, authentic experience."
    elif level == 2:
        recommendation = "Sweet spot — manageable crowds, good availability, fair prices."
    elif level == 3:
        recommendation = "Busy season — book accommodation and transport at least 2 weeks ahead."
    elif level == 4:
        recommendation = "Peak season — very crowded, prices surge 30-50%, book a month ahead."
    else:
        recommendation = "No crowd data available."

    return {
        "destination": destination_key,
        "month": month,
        "crowd_label": info.get("label"),
        "recommendation": recommendation,
    }


def compare_months_for_destination(destination_key: str, months: list[int]) -> list:
    """
    Compares crowd levels across multiple months for a destination.
    Useful when user has flexible dates.
    """
    results = []
    for m in months:
        info = get_crowd_info(destination_key, m)
        results.append(info)

    # Sort by crowd level (quietest first)
    from data.peak_seasons import CROWD_LEVELS
    results.sort(key=lambda x: CROWD_LEVELS.get(x["destination"], [0]*13)[x["month"]])
    return results
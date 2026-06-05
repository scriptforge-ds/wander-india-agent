# Crowd level by destination and month
# 1 = very quiet, 2 = moderate, 3 = busy, 4 = very crowded

CROWD_LEVELS = {
    "kedarkantha":      [0, 4, 3, 2, 3, 2, 1, 0, 0, 1, 2, 3, 4],
    "coorg":            [0, 3, 3, 2, 1, 1, 1, 2, 2, 2, 3, 4, 4],
    "spiti":            [0, 1, 1, 1, 1, 1, 3, 4, 4, 3, 1, 1, 1],
    "hampi":            [0, 3, 3, 2, 2, 1, 1, 1, 1, 1, 2, 3, 4],
    "chopta":           [0, 2, 2, 3, 4, 3, 2, 2, 2, 2, 4, 3, 2],
    "gokarna":          [0, 3, 3, 2, 1, 1, 1, 1, 1, 1, 2, 3, 4],
    "ladakh":           [0, 1, 1, 1, 1, 1, 3, 4, 4, 2, 1, 1, 1],
    "majuli":           [0, 2, 2, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3],
    "chikmagalur":      [0, 3, 3, 2, 2, 1, 1, 1, 1, 2, 3, 4, 4],
    "valley_of_flowers":[0, 0, 0, 0, 0, 0, 3, 4, 3, 1, 0, 0, 0],
}

CROWD_LABELS = {
    0: "❌ Closed / Inaccessible",
    1: "🟢 Very Quiet — Offbeat",
    2: "🟡 Moderate — Sweet Spot",
    3: "🟠 Busy — Book Ahead",
    4: "🔴 Peak Season — Crowded & Expensive",
}


def get_crowd_level(destination_key: str, month: int) -> dict:
    """
    Returns crowd level and label for a destination in a given month.
    month: 1-12
    """
    levels = CROWD_LEVELS.get(destination_key)
    if not levels:
        return {"level": None, "label": "No data available"}

    level = levels[month]
    return {
        "level": level,
        "label": CROWD_LABELS[level],
        "destination": destination_key,
        "month": month,
    }
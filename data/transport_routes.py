# Major budget transport routes in India
# cost in ₹, duration in hours

TRANSPORT_ROUTES = {
    ("bangalore", "coorg"): {
        "bus": {"cost": 300, "duration": 5, "operator": "KSRTC"},
        "cab": {"cost": 2500, "duration": 4.5},
    },
    ("bangalore", "chikmagalur"): {
        "bus": {"cost": 250, "duration": 4, "operator": "KSRTC"},
        "cab": {"cost": 2200, "duration": 3.5},
    },
    ("bangalore", "gokarna"): {
        "bus": {"cost": 500, "duration": 9, "operator": "KSRTC"},
        "train": {"cost": 200, "duration": 8, "train": "Goa Express"},
    },
    ("bangalore", "hampi"): {
        "bus": {"cost": 400, "duration": 7, "operator": "KSRTC"},
        "train": {"cost": 250, "duration": 6.5, "train": "Hampi Express"},
    },
    ("delhi", "rishikesh"): {
        "bus": {"cost": 400, "duration": 6, "operator": "UPSRTC/GMOU"},
        "train": {"cost": 200, "duration": 5.5, "train": "Shatabdi/Jan Shatabdi"},
    },
    ("rishikesh", "sankri"): {
        "bus": {"cost": 350, "duration": 8, "operator": "Local buses + shared jeep"},
        "cab": {"cost": 3500, "duration": 7},
    },
    ("rishikesh", "chopta"): {
        "bus": {"cost": 250, "duration": 5, "operator": "Local bus via Ukhimath"},
        "cab": {"cost": 2800, "duration": 4.5},
    },
    ("shimla", "kaza"): {
        "bus": {"cost": 600, "duration": 12, "operator": "HRTC"},
        "cab": {"cost": 6000, "duration": 10},
    },
    ("manali", "kaza"): {
        "bus": {"cost": 500, "duration": 9, "operator": "HRTC (seasonal)"},
        "cab": {"cost": 5000, "duration": 8},
    },
    ("jorhat", "majuli"): {
        "ferry": {"cost": 20, "duration": 1, "operator": "State ferry"},
        "cab": {"cost": 300, "duration": 1.5},
    },
    ("leh", "leh"): {
        "flight_delhi": {"cost": 4000, "duration": 1.5, "note": "Book 2 months ahead for budget fares"},
        "bus_manali": {"cost": 700, "duration": 20, "operator": "HRTC (seasonal)"},
    },
}


def get_route(origin: str, destination: str) -> dict:
    """
    Returns transport options between two cities.
    Case-insensitive lookup.
    """
    key = (origin.lower(), destination.lower())
    reverse_key = (destination.lower(), origin.lower())

    route = TRANSPORT_ROUTES.get(key) or TRANSPORT_ROUTES.get(reverse_key)

    if not route:
        return {"error": f"No route data for {origin} → {destination}"}

    return route
import os
import json
from google import genai
from google.genai import types
from agent.system_prompt import SYSTEM_PROMPT
from agent.context_manager import build_context
from agent.tools.weather_tool import get_weather_for_destination
from agent.tools.crowd_tool import get_crowd_info, compare_months_for_destination
from agent.tools.places_tool import search_destinations, get_destination_detail
from agent.tools.transport_tool import get_transport_options, estimate_transport_cost_for_trip
from agent.tools.budget_tool import calculate_full_trip_budget, check_budget_feasibility
from agent.tools.maps_tool import CITY_COORDS, DESTINATION_COORDS

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ─── Tool Schemas ────────────────────────────────────────────────────────────

TOOL_SCHEMAS = [
    types.Tool(function_declarations=[

        types.FunctionDeclaration(
            name="search_destinations",
            description="Search and filter Indian travel destinations based on trip type, month, budget, region, and difficulty.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "trip_type": types.Schema(
                        type=types.Type.STRING,
                        description="Type of trip: trek, vacation, camping, road_trip"
                    ),
                    "month": types.Schema(
                        type=types.Type.INTEGER,
                        description="Travel month as integer (1=Jan, 12=Dec)"
                    ),
                    "max_daily_budget": types.Schema(
                        type=types.Type.INTEGER,
                        description="Maximum daily budget per person in INR"
                    ),
                    "region": types.Schema(
                        type=types.Type.STRING,
                        description="Region: north, south, northeast"
                    ),
                    "difficulty": types.Schema(
                        type=types.Type.STRING,
                        description="Trek difficulty: easy, easy-moderate, moderate, challenging"
                    ),
                },
            ),
        ),

        types.FunctionDeclaration(
            name="get_destination_detail",
            description="Get full details about a specific destination by its key.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "destination_key": types.Schema(
                        type=types.Type.STRING,
                        description="Destination key e.g. coorg, spiti, hampi, kedarkantha"
                    ),
                },
                required=["destination_key"],
            ),
        ),

        types.FunctionDeclaration(
            name="get_weather_for_destination",
            description="Get historical climate data (temperature, rainfall) for a destination in specific months.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "destination_key": types.Schema(
                        type=types.Type.STRING,
                        description="Destination key e.g. coorg, spiti, hampi"
                    ),
                    "months": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.INTEGER),
                        description="List of months as integers e.g. [10, 11, 12]"
                    ),
                },
                required=["destination_key", "months"],
            ),
        ),

        types.FunctionDeclaration(
            name="get_crowd_info",
            description="Get crowd level and travel recommendation for a destination in a specific month.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "destination_key": types.Schema(
                        type=types.Type.STRING,
                        description="Destination key e.g. coorg, spiti, hampi"
                    ),
                    "month": types.Schema(
                        type=types.Type.INTEGER,
                        description="Month as integer (1-12)"
                    ),
                },
                required=["destination_key", "month"],
            ),
        ),

        types.FunctionDeclaration(
            name="get_transport_options",
            description="Get available transport options (bus, train, cab) between two cities with cost and duration.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Origin city in lowercase e.g. bangalore, delhi, mumbai"
                    ),
                    "destination": types.Schema(
                        type=types.Type.STRING,
                        description="Destination city or key in lowercase"
                    ),
                },
                required=["origin", "destination"],
            ),
        ),

        types.FunctionDeclaration(
            name="check_budget_feasibility",
            description="Check if a user's total budget is sufficient for a trip and get a full cost breakdown.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "total_budget": types.Schema(
                        type=types.Type.INTEGER,
                        description="User's total budget in INR"
                    ),
                    "destination_key": types.Schema(
                        type=types.Type.STRING,
                        description="Destination key e.g. coorg, spiti, hampi"
                    ),
                    "days": types.Schema(
                        type=types.Type.INTEGER,
                        description="Number of days"
                    ),
                    "people": types.Schema(
                        type=types.Type.INTEGER,
                        description="Number of people travelling"
                    ),
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Origin city in lowercase (optional)"
                    ),
                },
                required=["total_budget", "destination_key", "days", "people"],
            ),
        ),

        types.FunctionDeclaration(
            name="calculate_full_trip_budget",
            description="Calculate complete trip cost breakdown for a destination including stay, food, transport and misc.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "destination_key": types.Schema(
                        type=types.Type.STRING,
                        description="Destination key e.g. coorg, spiti, hampi"
                    ),
                    "days": types.Schema(
                        type=types.Type.INTEGER,
                        description="Number of days"
                    ),
                    "people": types.Schema(
                        type=types.Type.INTEGER,
                        description="Number of people"
                    ),
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Origin city in lowercase (optional)"
                    ),
                },
                required=["destination_key", "days", "people"],
            ),
        ),

    ])
]

# ─── Tool Executor ────────────────────────────────────────────────────────────

def execute_tool(tool_name: str, tool_args: dict) -> str:
    """
    Routes tool call from Gemini to the correct Python function.
    Returns result as JSON string.
    """
    try:
        if tool_name == "search_destinations":
            result = search_destinations(**tool_args)

        elif tool_name == "get_destination_detail":
            result = get_destination_detail(**tool_args)

        elif tool_name == "get_weather_for_destination":
            result = get_weather_for_destination(**tool_args)

        elif tool_name == "get_crowd_info":
            result = get_crowd_info(**tool_args)

        elif tool_name == "get_transport_options":
            result = get_transport_options(**tool_args)

        elif tool_name == "check_budget_feasibility":
            result = check_budget_feasibility(**tool_args)

        elif tool_name == "calculate_full_trip_budget":
            result = calculate_full_trip_budget(**tool_args)

        else:
            result = {"error": f"Unknown tool: {tool_name}"}

        return json.dumps(result, default=str)

    except Exception as e:
        return json.dumps({"error": str(e)})


# ─── Main Orchestrator ────────────────────────────────────────────────────────

def get_response(messages: list) -> str:
    """
    Agentic loop:
    1. Send messages to Gemini
    2. If Gemini calls a tool → execute it → send result back
    3. Repeat until Gemini returns a final text response
    """
    try:
        history = build_context(messages)
        chat_history = history[:-1]
        last_message = history[-1]["parts"][0]["text"]

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=TOOL_SCHEMAS,
            ),
            history=chat_history,
        )

        response = chat.send_message(last_message)

        # Agentic loop — keep going until no more tool calls
        while True:
            tool_calls = [
                part for part in response.candidates[0].content.parts
                if hasattr(part, "function_call") and part.function_call
            ]

            if not tool_calls:
                # No tool calls — Gemini is done, return final text
                return response.text

            # Execute all tool calls in this round
            tool_results = []
            for part in tool_calls:
                fn = part.function_call
                print(f"[Tool Call] Executing: {fn.name} with args: {dict(fn.args)}")
                tool_output = execute_tool(fn.name, dict(fn.args))
                tool_results.append(
                    types.Part.from_function_response(
                        name=fn.name,
                        response={"result": tool_output}
                    )
                )

            # Send tool results back to Gemini
            response = chat.send_message(tool_results)

    except Exception as e:
        return f"Sorry, something went wrong: {str(e)}"
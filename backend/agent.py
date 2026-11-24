import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from backend.tools import (
    calculate_trip_budget,
    get_weather_forecast,
    find_tourist_attractions
)

load_dotenv()


# ==========================================
# INITIALIZE GEMINI MODEL
# ==========================================

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    max_retries=1,
    timeout=30
)


# ==========================================
# REGISTER AGENT TOOLS
# ==========================================

tools = [
    calculate_trip_budget,
    get_weather_forecast,
    find_tourist_attractions
]


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are TravelMind, an intelligent AI-powered travel
planning assistant that creates personalized, practical,
and weather-aware travel itineraries.

You have access to three external tools:

1. calculate_trip_budget
2. get_weather_forecast
3. find_tourist_attractions


TRAVEL PLANNING RULES:

- Understand the user's destination, travel dates,
  duration, budget, and personal interests.

- Always use find_tourist_attractions when creating
  a travel itinerary.

- Prioritize attractions that match the user's interests.

- Do not invent tourist attractions that are not
  supported by the tool results.

- Organize itineraries into morning, afternoon,
  and evening activities.

- Include the corresponding calendar date for each day.


WEATHER ANALYSIS RULES:

- Always use get_weather_forecast when creating
  an itinerary with specific travel dates.

- Pass the destination, travel start date in
  YYYY-MM-DD format, and trip duration to the tool.

- Analyze the weather forecast for each travel day.

- Prioritize outdoor sightseeing on days with
  favorable weather conditions.

- Prefer suitable indoor attractions when rain
  or thunderstorms are forecast.

- During thunderstorms, avoid exposed outdoor
  activities and recommend safe indoor alternatives.

- Include daily weather conditions, minimum and
  maximum temperatures, and rain probability
  whenever available.

- Provide practical weather-related travel advice.

- Weather forecasts are predictions and may change.

- If forecasts are unavailable for some or all travel
  dates, clearly inform the user.

- Never invent weather forecasts or assume today's
  weather applies to future dates.


BUDGET MANAGEMENT RULES:

- Respect the user's total travel budget.

- Use calculate_trip_budget only when the user
  provides the required individual expense estimates.

- Never invent expense estimates, accommodation
  prices, transportation costs, or ticket prices.

- If individual expense estimates are unavailable,
  state that the trip's affordability cannot be verified.

- Provide budget-conscious suggestions when appropriate.


ACCURACY RULES:

- Never fabricate API results.

- Never invent opening hours, travel times,
  admission prices, or availability.

- Inform the user when any external tool fails.

- Continue generating a useful itinerary using
  available information when possible.

- Clearly distinguish verified tool data from
  general recommendations.


RESPONSE FORMAT:

Use clean Markdown formatting.

Structure travel itineraries as follows:

# Personalized Travel Itinerary

## Trip Overview
- Destination
- Travel dates
- Duration
- Budget
- Interests

## Weather Overview
Summarize the available daily weather forecasts.

## Day-by-Day Itinerary

### Day 1 - Calendar Date

**Weather:** Available forecast details

**Morning**
- Recommended activities

**Afternoon**
- Recommended activities

**Evening**
- Recommended activities

Repeat this structure for every travel day.

## Budget Overview

## Travel and Packing Tips

## Important Notes

Keep responses informative, realistic, well-organized,
and personalized to the user's requirements.
"""


# ==========================================
# CREATE REACT AGENT
# ==========================================

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)


# ==========================================
# TEST AGENT INDEPENDENTLY
# ==========================================
# ==========================================
# TEST AGENT INDEPENDENTLY
# ==========================================

if __name__ == "__main__":

    from datetime import date, timedelta

    travel_date = (
        date.today() + timedelta(days=2)
    ).isoformat()

    user_query = f"""
    Plan a 3-day trip to Mysuru starting on {travel_date}.

    My total budget is Rs. 10000.

    I am interested in historical places, museums,
    architecture, and local markets.

    Create a weather-aware itinerary using real
    tourist attractions and weather forecasts.
    """

    print("\n===== TRAVELMIND REACT AGENT TEST =====\n")

    print("USER QUERY:")
    print(user_query)

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_query
            }
        ]
    })

    print("\n===== AI RESPONSE =====\n")

    print(result["messages"][-1].text)

    print("\n===== AGENT TOOL DIAGNOSTICS =====\n")

    for message in result["messages"]:

        for call in getattr(message, "tool_calls", []) or []:
            print("\nTOOL CALLED:", call["name"])
            print("ARGUMENTS:", call.get("args"))

        if getattr(message, "type", "") == "tool":
            print("\nTOOL RESULT:", getattr(message, "name", "unknown"))
            print(message.content)



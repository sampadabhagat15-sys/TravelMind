import os
import requests
import time

from datetime import date, datetime, timedelta, timezone
from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()


# ==========================================
# TOOL 1: TRAVEL BUDGET CALCULATOR
# ==========================================

@tool
def calculate_trip_budget(
    total_budget: float,
    transportation: float,
    accommodation: float,
    food: float,
    activities: float,
    other: float = 0
) -> dict:
    """
    Calculate total travel expenses and determine
    whether a trip is within the user's budget.
    All expenses must be for the entire trip
    and must use the same currency.
    """

    expenses = {
        "transportation": transportation,
        "accommodation": accommodation,
        "food": food,
        "activities": activities,
        "other": other
    }

    if total_budget < 0 or any(
        value < 0 for value in expenses.values()
    ):
        return {
            "error": "Budget and expenses cannot be negative."
        }

    total_cost = round(sum(expenses.values()), 2)
    remaining_budget = round(total_budget - total_cost, 2)
    within_budget = remaining_budget >= 0

    return {
        "total_budget": total_budget,
        "total_cost": total_cost,
        "remaining_budget": remaining_budget,
        "within_budget": within_budget,
        "expense_breakdown": expenses,
        "status": (
            "Within budget"
            if within_budget
            else "Budget exceeded"
        )
    }


# ==========================================
# WEATHER CODE INTERPRETATION
# ==========================================

def interpret_weather_code(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",
        56: "Light freezing drizzle",
        57: "Heavy freezing drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Light snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",
        77: "Snow grains",
        80: "Light rain showers",
        81: "Moderate rain showers",
        82: "Heavy rain showers",
        85: "Light snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with light hail",
        99: "Thunderstorm with heavy hail"
    }

    return weather_codes.get(code, "Unknown weather condition")


def weather_request(url, params):
    """Retry transient weather-service failures, at most two attempts."""
    for attempt in range(2):
        try:
            response = requests.get(url, params=params, timeout=(5, 15))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:
            status = exc.response.status_code if exc.response is not None else None
            retryable = (
                status in (500, 502, 503, 504)
                or isinstance(exc, (requests.exceptions.Timeout,
                                    requests.exceptions.ConnectionError))
            )
            if not retryable or attempt == 1:
                raise
            time.sleep(1 + attempt)


# ==========================================
# TOOL 2: DATE-SPECIFIC WEATHER FORECAST
# ==========================================

def _open_meteo_forecast(
    city: str,
    start_date: str = "",
    duration: int = 1
) -> dict:
    """
    Get real weather forecasts for a destination
    and specific travel dates.

    Args:
        city: Destination city name.
        start_date: Travel start date in YYYY-MM-DD
                    format. Defaults to today.
        duration: Number of travel days.

    Forecasts are available up to 16 days
    including today. Dates outside the forecast
    window must not be treated as confirmed weather.
    """

    stage = "geocoding"
    try:

        if duration < 1 or duration > 30:
            return {
                "error": "Duration must be between 1 and 30 days."
            }

        # STEP 1: GET CITY COORDINATES

        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
        )

        geo_data = weather_request(
            geo_url,
            params={
                "name": city,
                "count": 1,
                "language": "en",
                "format": "json"
            }
        )


        if not geo_data.get("results"):
            return {
                "error": f"Location '{city}' could not be found."
            }

        location = geo_data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # STEP 2: GET DAILY WEATHER FORECAST

        stage = "forecast"
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
        )

        weather_data = weather_request(
            weather_url,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": (
                    "weather_code,"
                    "temperature_2m_max,"
                    "temperature_2m_min,"
                    "precipitation_probability_max"
                ),
                "forecast_days": 16,
                "timezone": "auto"
            }
        )


        daily = weather_data.get("daily", {})
        available_dates = daily.get("time", [])

        if not available_dates:
            return {
                "error": "Weather forecast data is unavailable."
            }

        stage = "forecast processing"
        # STEP 3: VALIDATE TRAVEL DATES

        today = date.fromisoformat(available_dates[0])

        if start_date:
            try:
                trip_start = datetime.strptime(
                    start_date, "%Y-%m-%d"
                ).date()

            except ValueError:
                return {
                    "error": "Use YYYY-MM-DD date format."
                }
        else:
            trip_start = today

        trip_end = trip_start + timedelta(days=duration - 1)

        if trip_start < today:
            return {
                "error": "Past travel dates are not supported."
            }

        # STEP 4: PROCESS EACH TRAVEL DAY

        forecasts = []
        unavailable_dates = []

        for day_number in range(duration):

            current_date = trip_start + timedelta(
                days=day_number
            )

            formatted_date = current_date.isoformat()

            if formatted_date in available_dates:

                index = available_dates.index(
                    formatted_date
                )

                weather_code = daily["weather_code"][index]

                forecasts.append({
                    "day": day_number + 1,
                    "date": formatted_date,
                    "condition": interpret_weather_code(
                        weather_code
                    ),
                    "max_temperature_c": (
                        daily["temperature_2m_max"][index]
                    ),
                    "min_temperature_c": (
                        daily["temperature_2m_min"][index]
                    ),
                    "rain_probability_percent": (
                        daily[
                            "precipitation_probability_max"
                        ][index]
                    )
                })

            else:
                unavailable_dates.append(formatted_date)

        # STEP 5: RETURN STRUCTURED RESULTS

        return {
            "city": location["name"],
            "country": location.get("country", ""),
            "latitude": latitude,
            "longitude": longitude,
            "timezone": weather_data.get("timezone"),
            "travel_start_date": trip_start.isoformat(),
            "travel_end_date": trip_end.isoformat(),
            "forecast_available_until": available_dates[-1],
            "forecasts": forecasts,
            "unavailable_dates": unavailable_dates,
            "status": (
                "Forecast unavailable for all travel dates"
                if not forecasts
                else "Partial forecast available"
                if unavailable_dates
                else "Complete forecast available"
            ),
            "note": (
                "Weather forecasts are predictions and "
                "may change closer to the travel date. "
                "Do not invent weather conditions for "
                "unavailable dates."
            )
        }

    except requests.exceptions.RequestException as exc:
        status = exc.response.status_code if exc.response is not None else None
        category = type(exc).__name__
        print(f"Weather failure: stage={stage}, type={category}, HTTP={status}", flush=True)
        return {
            "error": "Weather service request failed.",
            "stage": stage,
            "error_type": category,
            "http_status": status
        }

    except Exception as exc:
        category = type(exc).__name__
        print(f"Weather failure: stage={stage}, type={category}", flush=True)
        return {
            "error": "Unable to process the weather forecast.",
            "stage": stage,
            "error_type": category
        }


# In-memory cache, shared by requests within this backend process.
from copy import deepcopy
from threading import Lock

_weather_cache = {}
_weather_lock = Lock()


def _fallback_weather(city, start_date, duration):
    key = os.getenv('WEATHERAPI_KEY')
    if not key:
        return {'error': 'Fallback weather API key is missing.'}
    try:
        response = requests.get(
            'https://api.weatherapi.com/v1/forecast.json',
            params={'key': key, 'q': city, 'days': 3, 'aqi': 'no', 'alerts': 'no'},
            timeout=(5, 12))
        response.raise_for_status()
        data = response.json()
        location = data['location']
        today = date.fromisoformat(location['localtime'][:10])
        start = date.fromisoformat(start_date) if start_date else today
        if start < today:
            return {'error': 'Past travel dates are not supported.'}
        days = {d['date']: d['day'] for d in data['forecast']['forecastday']}
        forecasts, missing = [], []
        for i in range(duration):
            day = (start + timedelta(days=i)).isoformat()
            if day not in days:
                missing.append(day)
                continue
            d = days[day]
            forecasts.append({'day': i+1, 'date': day,
                'condition': d['condition']['text'],
                'max_temperature_c': d.get('maxtemp_c'),
                'min_temperature_c': d.get('mintemp_c'),
                'rain_probability_percent': d.get('daily_chance_of_rain'),
                'source': 'WeatherAPI.com'})
        return {'city': location['name'], 'country': location['country'],
            'latitude': location['lat'], 'longitude': location['lon'],
            'timezone': location['tz_id'], 'travel_start_date': start.isoformat(),
            'travel_end_date': (start + timedelta(days=duration-1)).isoformat(),
            'forecast_available_until': max(days, default=None),
            'forecasts': forecasts, 'unavailable_dates': missing,
            'source': 'WeatherAPI.com',
            'status': ('Forecast unavailable for all travel dates' if not forecasts else
                       'Partial forecast available' if missing else 'Complete forecast available'),
            'note': 'Fallback forecasts cover up to three days including today. Do not invent weather for unavailable dates.'}
    except Exception as exc:
        # Never expose exception URLs, which may contain the API key.
        response = getattr(exc, 'response', None)
        return {'error': 'Fallback weather service failed.',
                'http_status': response.status_code if response is not None else None,
                'error_type': type(exc).__name__}


@tool
def get_weather_forecast(city: str, start_date: str = '', duration: int = 1) -> dict:
    """Get real daily weather for a city and travel dates (YYYY-MM-DD), for 1–30 days. Uses Open-Meteo and a WeatherAPI fallback. Never invent unavailable forecasts."""
    if not city.strip() or not 1 <= duration <= 30:
        return {'error': 'Provide a city and duration between 1 and 30 days.'}
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date().isoformat()
        except ValueError:
            return {'error': 'Use YYYY-MM-DD date format.'}
    cache_key = (city.strip().casefold(), start_date, duration)
    now = time.monotonic()
    with _weather_lock:
        cached = _weather_cache.get(cache_key)
        if cached and now - cached[0] < 900:
            result = deepcopy(cached[1])
            result['cached'] = True
            return result
    primary = _open_meteo_forecast(city, start_date, duration)
    if 'error' not in primary:
        result = primary
        result['source'] = 'Open-Meteo'
    elif primary.get('error') == 'Past travel dates are not supported.':
        return primary
    else:
        result = _fallback_weather(city, start_date, duration)
        if 'error' in result:
            return {'error': 'Both weather providers failed.', 'primary': primary, 'fallback': result}
    result['cached'] = False
    result['retrieved_at_utc'] = datetime.now(timezone.utc).isoformat()
    if result.get('forecasts'):
        with _weather_lock:
            if len(_weather_cache) >= 256:
                _weather_cache.pop(next(iter(_weather_cache)))
            _weather_cache[cache_key] = (time.monotonic(), deepcopy(result))
    return result


# ==========================================
# TOOL 3: TOURIST ATTRACTION FINDER
# ==========================================

@tool
def find_tourist_attractions(city: str) -> dict:
    """
    Find real tourist attractions near a destination
    using the OpenTripMap API.
    """

    api_key = os.getenv("OPENTRIPMAP_API_KEY")

    if not api_key:
        return {
            "error": "OpenTripMap API key is missing."
        }

    base_url = (
        "https://api.opentripmap.com/0.1/en/places"
    )

    try:

        # STEP 1: GET CITY COORDINATES

        geo_response = requests.get(
            f"{base_url}/geoname",
            params={
                "name": city,
                "apikey": api_key
            },
            timeout=15
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if "lat" not in geo_data or "lon" not in geo_data:
            return {
                "error": f"Could not locate '{city}'."
            }

        latitude = geo_data["lat"]
        longitude = geo_data["lon"]

        # STEP 2: FIND NEARBY ATTRACTIONS

        attractions_response = requests.get(
            f"{base_url}/radius",
            params={
                "radius": 10000,
                "lon": longitude,
                "lat": latitude,
                "rate": 2,
                "limit": 20,
                "format": "json",
                "apikey": api_key
            },
            timeout=20
        )

        attractions_response.raise_for_status()
        attractions_data = attractions_response.json()

        attractions = []
        seen_names = set()

        # STEP 3: FILTER AND ORGANIZE RESULTS

        for place in attractions_data:

            name = place.get("name", "").strip()

            if not name or name.lower() in seen_names:
                continue

            seen_names.add(name.lower())

            point = place.get("point", {})

            attractions.append({
                "name": name,
                "category": place.get("kinds", ""),
                "latitude": point.get("lat"),
                "longitude": point.get("lon"),
                "xid": place.get("xid")
            })

            if len(attractions) >= 10:
                break

        return {
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "total_attractions": len(attractions),
            "attractions": attractions,
            "note": (
                "Opening hours, ticket prices and public "
                "access have not been verified."
            )
        }

    except requests.exceptions.RequestException:
        return {
            "error": "Unable to connect to OpenTripMap."
        }

    except Exception:
        return {
            "error": "Unable to retrieve tourist attractions."
        }


# ==========================================
# TEST WEATHER TOOL INDEPENDENTLY
# ==========================================

if __name__ == "__main__":

    from pprint import pprint

    test_date = (
        date.today() + timedelta(days=2)
    ).isoformat()

    print("\n===== TRAVELMIND WEATHER TOOL TEST =====\n")

    result = get_weather_forecast.invoke({
        "city": "Mysuru",
        "start_date": test_date,
        "duration": 3
    })

    pprint(result)




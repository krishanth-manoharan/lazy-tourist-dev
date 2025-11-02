# Data Directory

This directory contains API endpoint configurations for external data sources.

## Files

### `apis.py`
Contains all external API endpoint URLs used by the application.

#### Current APIs:
- **OUTBOUND_FLIGHTS_API**: GET endpoint for fetching outbound flight data
  - URL: `https://mocki.io/v1/4af942e2-77af-49c1-993c-226c010f6d80`
  - Used by: `tools/flight_tools.py::search_flights()`
  - Query Params: `origin`, `destination`, `departure_date`, `passengers`
  - Source: API is the primary and only source (no fallback to mocks)

- **RETURN_FLIGHTS_API**: GET endpoint for fetching return flight data
  - URL: `https://mocki.io/v1/51b1bee3-c204-43bc-ac1b-f392bfc1d225`
  - Used by: `tools/flight_tools.py::search_return_flights()`
  - Query Params: `origin`, `destination`, `return_date`, `passengers`
  - Source: API is the primary and only source (no fallback to mocks)

- **HOTELS_API**: GET endpoint for fetching hotel data
  - URL: `https://mocki.io/v1/d3ad52c6-401a-4662-9d9a-d85db96f0a46`
  - Used by: `tools/hotel_tools.py::search_hotels()`
  - Query Params: `location`, `check_in`, `check_out`, `guests`
  - Source: API is the primary and only source (no fallback to mocks)

- **ACTIVITIES_API**: GET endpoint for fetching activities and attractions
  - URL: `https://mocki.io/v1/c98f68ba-55a2-4d93-8acf-62d699a7b428`
  - Used by: `tools/activity_tools.py::search_activities()`
  - Query Params: `location`, `interests`, `max_price`
  - Source: API is the primary and only source (no fallback to mocks)

- **DESTINATION_INFO_API**: GET endpoint for fetching destination information
  - URL: `https://mocki.io/v1/0333b0f3-2fe3-497d-8efa-6d65cfee7b70`
  - Used by: `tools/activity_tools.py::get_destination_info()`
  - Query Params: `location`
  - Source: API is the primary and only source (no fallback to mocks)

## Usage Pattern

### Direct API Call (Primary Method)
```python
from data.apis import RETURN_FLIGHTS_API
from utils.api_client import fetch_api_data
from urllib.parse import urlencode

# Fetch data directly from API with query parameters appended to URL
try:
    query_params = urlencode({
        "origin": "Paris",
        "destination": "NYC",
        "return_date": "2025-06-20",
        "passengers": 2
    })
    api_url = f"{RETURN_FLIGHTS_API}?{query_params}"
    data = fetch_api_data(url=api_url)
except Exception as e:
    # Handle error appropriately
    print(f"Error: {e}")
```

**Note**: Query parameters are appended directly to the URL for demo purposes to show proper API usage patterns. The mock API responses won't change based on these parameters, but in production with real APIs, these parameters would filter and customize the results.

### With Fallback (Optional Pattern)
```python
from data.apis import RETURN_FLIGHTS_API
from utils.api_client import fetch_api_data_with_fallback

# Fetch data with automatic fallback to mock data
data = fetch_api_data_with_fallback(
    url=RETURN_FLIGHTS_API,
    fallback_data=mock_data
)
```

## Adding New APIs

To add a new external API:

1. Add the endpoint URL to `apis.py`:
```python
NEW_API_ENDPOINT = "https://api.example.com/endpoint"
```

2. Use the API in your tool:
```python
from data.apis import NEW_API_ENDPOINT
from utils.api_client import fetch_api_data_with_fallback

data = fetch_api_data_with_fallback(
    url=NEW_API_ENDPOINT,
    fallback_data=your_mock_data
)
```

## API Response Format

External APIs should return JSON in a format compatible with the application's data schemas.

Both outbound and return flight APIs use the same route-based structure:

**Outbound Flights Example (NYC → Paris):**
```json
{
  "NYC-PARIS": [
    {
      "airline": "Air France",
      "flight_number": "AF007",
      "departure": "JFK",
      "arrival": "CDG",
      "duration": "7h 30m",
      "price": 650,
      "stops": 0,
      "departure_time": "22:30",
      "arrival_time": "12:00+1"
    }
  ],
  "NYC-BALI": [...],
  "NYC-TOKYO": [...],
  "DEFAULT": [...]
}
```

**Return Flights Example (Paris → NYC):**
```json
{
  "PARIS-NYC": [
    {
      "airline": "Air France",
      "flight_number": "AF008",
      "departure": "CDG",
      "arrival": "JFK",
      "duration": "8h 45m",
      "price": 680,
      "stops": 0,
      "departure_time": "14:30",
      "arrival_time": "17:15"
    }
  ],
  "BALI-NYC": [...],
  "TOKYO-NYC": [...],
  "DEFAULT": [...]
}
```

**Route Matching Logic:**
1. Normalize the search (e.g., `NYC → Paris` becomes `NYC-PARIS`)
2. Look for exact route match in the API response
3. Try partial matches if exact match not found
4. Fall back to `DEFAULT` route if no match found


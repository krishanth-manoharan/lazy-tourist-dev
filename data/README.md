# Data Directory

This directory contains API endpoint configurations for external data sources.

## Files

### `apis.py`
Contains all external API endpoint URLs used by the application.

#### Current APIs:
- **OUTBOUND_FLIGHTS_API**: GET endpoint for fetching outbound flight data
  - URL: `https://mocki.io/v1/4af942e2-77af-49c1-993c-226c010f6d80`
  - Used by: `tools/flight_tools.py::search_flights()`
  - Source: API is the primary and only source (no fallback to mocks)

- **RETURN_FLIGHTS_API**: GET endpoint for fetching return flight data
  - URL: `https://mocki.io/v1/51b1bee3-c204-43bc-ac1b-f392bfc1d225`
  - Used by: `tools/flight_tools.py::search_return_flights()`
  - Source: API is the primary and only source (no fallback to mocks)

## Usage Pattern

### Direct API Call (Primary Method)
```python
from data.apis import RETURN_FLIGHTS_API
from utils.api_client import fetch_api_data

# Fetch data directly from API
try:
    data = fetch_api_data(url=RETURN_FLIGHTS_API)
except Exception as e:
    # Handle error appropriately
    print(f"Error: {e}")
```

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


"""
Utility functions for making external API calls
"""
import requests
import json
from typing import Dict, Any, Optional


def fetch_api_data(url: str, method: str = "GET", params: Optional[Dict[str, Any]] = None, 
                   headers: Optional[Dict[str, str]] = None, timeout: int = 10) -> Dict[str, Any]:
    """
    Make an external API call and return the response data.
    
    Args:
        url: The API endpoint URL
        method: HTTP method (GET, POST, etc.). Default: GET
        params: Query parameters for GET or body for POST
        headers: Optional HTTP headers
        timeout: Request timeout in seconds. Default: 10
    
    Returns:
        Dictionary containing the API response data
    
    Raises:
        requests.exceptions.RequestException: If the API call fails
    """
    try:
        print(f"🌐 Fetching data from external API: {url}")
        
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method.upper() == "POST":
            response = requests.post(url, json=params, headers=headers, timeout=timeout)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Raise an exception for bad status codes
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        print(f"✅ Successfully fetched data from API")
        
        return data
        
    except requests.exceptions.Timeout:
        print(f"❌ API request timed out after {timeout} seconds")
        raise
    except requests.exceptions.ConnectionError:
        print(f"❌ Failed to connect to API: {url}")
        raise
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP error occurred: {e.response.status_code}")
        raise
    except json.JSONDecodeError:
        print(f"❌ Failed to parse JSON response from API")
        raise
    except Exception as e:
        print(f"❌ Unexpected error during API call: {str(e)}")
        raise


def fetch_api_data_with_fallback(url: str, fallback_data: Any, method: str = "GET", 
                                  params: Optional[Dict[str, Any]] = None,
                                  headers: Optional[Dict[str, str]] = None,
                                  timeout: int = 10) -> Any:
    """
    Make an external API call with fallback to mock data if the call fails.
    
    Args:
        url: The API endpoint URL
        fallback_data: Data to return if API call fails
        method: HTTP method (GET, POST, etc.). Default: GET
        params: Query parameters for GET or body for POST
        headers: Optional HTTP headers
        timeout: Request timeout in seconds. Default: 10
    
    Returns:
        API response data if successful, otherwise fallback_data
    """
    try:
        return fetch_api_data(url, method, params, headers, timeout)
    except Exception as e:
        print(f"⚠️  API call failed, using fallback data: {str(e)}")
        return fallback_data


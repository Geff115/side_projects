#!/usr/bin/env python3
"""
Getting weather information of a given place,
country, or area.

Utilizing Meteorsource API, and passing the
/find_places endpoints to fetch a particular information
based on the input location
"""

import os
import requests


def get_weather_info(location, language='en'):
    """Getting weather info from Meteorsource API"""
    # Fetching meteor source api key
    METEORSOURCE_API_KEY = os.getenv("METEORSOURCE_API_KEY")
    if not METEORSOURCE_API_KEY:
        return "ERROR: METEORSOURCE_API_KEY environment variable not set"

    # creating a dict with header for meteorsource request
    meteorsource_header = {
        'X-API-Key': METEORSOURCE_API_KEY
    }

    # creating a dictionary for the find_places endpoint
    meteorsource_findplaces_parameter = {
        'text': location
    }

    # Sending request to the find_places endpoint to get the place_id
    try:
        response1 = requests.get(
            "https://www.meteosource.com/api/v1/free/find_places",
            params=meteorsource_findplaces_parameter,
            headers=meteorsource_header
        )
        response1.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Network error occured: {e}")

    response_data1 = response1.json()

    # Fetching the place id from the response data
    try:
        place_id = response_data1[0]['place_id']
    except(IndexError, KeyError):
        raise SystemExit("ERROR: could not fetch place_id, please check location input")

    # creating a new dictionary for the url parameters for meteorsource
    meteorsource_point_parameter = {
        'place_id': place_id,
        'sections': 'daily',
        'units': 'metric',
        'language': language
    }

    # sending request to get the weather forcast for the place_id
    try:
        response2 = requests.get(
            'https://www.meteosource.com/api/v1/free/point',
            params=meteorsource_point_parameter,
            headers=meteorsource_header
        )
        response2.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(f"Network error occured: {e}")

    response_data2 = response2.json()
    try:
        first_day = response_data2['daily']['data'][0]
        forecast = [
            {
                "date": first_day["day"],
                "summary": first_day["summary"]
            }
        ]
    except(ValueError, KeyError):
        raise SystemExit("ERROR: could not fetch the weather information for the date and summary")

    return {"location": location, "forecast": forecast}

import requests


USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"


def get_earthquakes():
    response = requests.get(USGS_URL, timeout=30)

    response.raise_for_status()

    return response.json()
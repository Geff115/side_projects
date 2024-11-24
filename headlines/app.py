#!/usr/bin/env python3
"""
Working with the FastAPI framework
to serve data in the frontend
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from morning_updates import get_morning_updates
from weather import get_weather_info


app = FastAPI()
# Serving static files
app.mount("/static", StaticFiles(directory="static"), name="static")
# Enabling resource sharing
app.add_middleware (
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def index():
    """Homepage"""
    return {"Welcome": "Welcome to the morning updates App!"}


@app.get("/morning-updates")
def morning_updates():
    """Fetch and display latest headlines"""
    try:
        updates = get_morning_updates()
        if isinstance(updates, dict) and "error" in updates:
            return {"error": updates["error"]}

        return updates
    except Exception as e:
        return {"error": f"An unexpected error occured: {str(e)}"}


@app.get("/weather")
def weather_endpoint(location: str, language: str = 'en'):
    """Fetch weather for a given location and language"""
    try:
        return get_weather_info(location, language)
    except Exception as e:
        return {"error": str(e)}

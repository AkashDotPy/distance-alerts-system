import requests
import math
import schedule
import time

def moving_coordinates():
    response = requests.get("BUS API URL")
    response = response.json()

    longitude = response[0]["Longitude"]
    latitude = response[0]["Latitude"]
    bus_longitude = float(longitude)
    bus_latitude = float(latitude)
    return response, bus_longitude, bus_latitude

def fixed_coordinates():
    home_latitude = #insert home latitude here
    home_longitude = #insert home longitude here
    return home_latitude, home_longitude

def haversine(home_latitude, home_longitude, bus_longitude, bus_latitude):
    earth_radius = 6371

    home_latitude = math.radians(home_latitude)
    home_longitude = math.radians(home_longitude)
    bus_latitude = math.radians(bus_latitude)
    bus_longitude = math.radians(bus_longitude)

    dlat = bus_latitude - home_latitude
    dlon = bus_longitude - home_longitude
    hav_formula = math.sin(dlat/2)**2 + math.cos(bus_latitude) * math.cos(home_latitude) * math.sin(dlon/2)**2
    angle_bet_points = 2 * math.atan2(math.sqrt(hav_formula), math.sqrt(1-hav_formula))
    distance_km = earth_radius * angle_bet_points
    return distance_km
      
def distance_between(home_latitude, home_longitude, bus_longitude, bus_latitude):
    distance_km = haversine(home_latitude, home_longitude, bus_longitude, bus_latitude)
    distance_meter = distance_km * 1000
    print(f"Distance between the two locations is {distance_meter:.2f} meters")

    if distance_meter <= 100 :
        call_alert()

def call_alert():     
    key = "1b77dd81-25bc-4562-b2ad-2821db5b0435"
    secret = "HMcuEVecWkSSdWYgoKr2Pg=="
    fromNumber = "+447520662200"
    to = "contact number to recive alert call"
    locale = "IN"
    url = "https://calling.api.sinch.com/calling/v1/callouts"
    payload = {
      "method": "ttsCallout",
      "ttsCallout": {
        "cli": fromNumber,
        "destination": {
          "type": "number",
          "endpoint": to
        },
        "locale": locale,
        "text": "Hello, this is a call from Sinch. Congratulations! You made your first call."
      }
    }
    headers = { "Content-Type": "application/json" }
    response = requests.post(url, json=payload, headers=headers, auth=(key, secret))

if __name__ == "__main__":  
    home_latitude, home_longitude = fixed_coordinates()
    response, bus_longitude, bus_latitude = moving_coordinates()
    distance = distance_between(home_latitude, home_longitude, bus_longitude, bus_latitude )
    schedule.every(1).minutes.do(distance)
    while True:
      schedule.run_pending()
      time.sleep(1) 





import os
import zipfile
import urllib.request
import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import ssl
import certifi

# Fix SSL context for Windows Python
ssl._create_default_https_context = ssl._create_unverified_context
os.environ['SSL_CERT_FILE'] = certifi.where()

STATIC_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/7795b45e-e65a-4465-81fc-c36b9dfff169/resource/cfb6b2b8-6191-41e3-bda1-b175c51148cb/download/opendata_ttc_schedules.zip"
STATIC_ZIP = "ttc_static.zip"
STATIC_DIR = "google_transit"
RT_URL = "https://bustime.ttc.ca/gtfsrt/trips"

def fetch_static_data():
    print("--- Fetching Static Data ---")
    if not os.path.exists(STATIC_ZIP):
        print("Downloading static ZIP...")
        urllib.request.urlretrieve(STATIC_URL, STATIC_ZIP)
    else:
        print("Static ZIP already downloaded.")
    
    if not os.path.exists(STATIC_DIR):
        print("Extracting ZIP...")
        with zipfile.ZipFile(STATIC_ZIP, 'r') as zip_ref:
            zip_ref.extractall(STATIC_DIR)
    else:
        print("Static data already extracted.")
    
    print("Reading stops.txt...")
    stops_df = pd.read_csv(os.path.join(STATIC_DIR, 'stops.txt'))
    print(f"Total stops loaded: {len(stops_df)}")
    print(stops_df[['stop_id', 'stop_name']].head())
    print("\n")

def fetch_realtime_data():
    print("--- Fetching Real-Time Data (TripUpdates) ---")
    feed = gtfs_realtime_pb2.FeedMessage()
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RT_URL, headers=headers, verify=certifi.where())
        response.raise_for_status()
        feed.ParseFromString(response.content)
        
        count = 0
        print("Sample of 10 active trips with delay info:")
        for entity in feed.entity:
            if entity.HasField('trip_update'):
                trip = entity.trip_update.trip
                for stop_time_update in entity.trip_update.stop_time_update:
                    if stop_time_update.HasField('arrival'):
                        delay_secs = stop_time_update.arrival.delay
                        delay_mins = delay_secs / 60.0
                        print(f"Route: {trip.route_id} | Trip ID: {trip.trip_id} | Stop ID: {stop_time_update.stop_id} | Delay: {delay_mins:.1f} mins")
                        count += 1
                        break # Just show one update per trip
            if count >= 10:
                break
        if count == 0:
            print("No active trips found right now.")
    except Exception as e:
        print(f"Error fetching real-time data: {e}")

if __name__ == "__main__":
    fetch_static_data()
    fetch_realtime_data()

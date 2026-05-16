import pandas as pd
import requests
from google.transit import gtfs_realtime_pb2
import certifi
import ssl
from datetime import datetime
from zoneinfo import ZoneInfo

ssl._create_default_https_context = ssl._create_unverified_context
RT_URL = "https://bustime.ttc.ca/gtfsrt/trips"
TZ = ZoneInfo('America/Toronto')

def time_string_to_seconds(time_str):
    """Convert GTFS time string 'HH:MM:SS' to seconds past midnight"""
    try:
        h, m, s = map(int, str(time_str).split(':'))
        return h * 3600 + m * 60 + s
    except:
        return 0

def analyze_realtime():
    print("1. Fetching live data from TTC...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(RT_URL, headers=headers, verify=certifi.where())
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    
    live_updates = []
    
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip = entity.trip_update.trip
            
            if len(entity.trip_update.stop_time_update) > 0:
                stu = entity.trip_update.stop_time_update[0]
                
                unix_time = None
                if stu.HasField('departure') and stu.departure.time > 0:
                    unix_time = stu.departure.time
                elif stu.HasField('arrival') and stu.arrival.time > 0:
                    unix_time = stu.arrival.time
                    
                if unix_time:
                    dt = datetime.fromtimestamp(unix_time, tz=TZ)
                    seconds_past_midnight = dt.hour * 3600 + dt.minute * 60 + dt.second
                    
                    live_updates.append({
                        "trip_id": str(trip.trip_id),
                        "route_id": str(trip.route_id),
                        "stop_sequence": stu.stop_sequence,
                        "stop_id": str(stu.stop_id),
                        "actual_time_str": dt.strftime('%H:%M:%S'),
                        "actual_seconds": seconds_past_midnight
                    })
                    
    rt_df = pd.DataFrame(live_updates)
    print(f"-> Captured {len(rt_df)} live vehicle positions.")
    
    if len(rt_df) == 0:
        return

    print("2. Loading Static Schedule (stop_times.txt)... (This might take a few seconds)")
    static_df = pd.read_csv('google_transit/stop_times.txt', 
                            usecols=['trip_id', 'arrival_time', 'stop_sequence'],
                            dtype={'trip_id': str, 'arrival_time': str})
    
    print("3. Matching Live Data with Static Schedule...")
    merged = pd.merge(rt_df, static_df, on=['trip_id', 'stop_sequence'], how='inner')
    
    if len(merged) == 0:
        print("Error: Could not match any trips. The static schedule might be out of sync with the live data.")
        return
        
    print(f"-> Successfully matched {len(merged)} trips.")
    
    print("4. Calculating Delays...")
    merged['scheduled_seconds'] = merged['arrival_time'].apply(time_string_to_seconds)
    merged['delay_seconds'] = merged['actual_seconds'] - merged['scheduled_seconds']
    
    # Handle overnight wraparound logic
    merged.loc[merged['delay_seconds'] < -43200, 'delay_seconds'] += 86400
    merged.loc[merged['delay_seconds'] > 43200, 'delay_seconds'] -= 86400
    
    merged['delay_mins'] = merged['delay_seconds'] / 60.0
    
    def get_status(mins):
        if mins > 2:
            return f"Late by {mins:.1f} m"
        elif mins < -2:
            return f"Early by {abs(mins):.1f} m"
        else:
            return "On Time"
            
    merged['Status'] = merged['delay_mins'].apply(get_status)
    
    print("\n==================================")
    print("   TTC REAL-TIME DELAY REPORT ")
    print("==================================\n")
    
    late_count = len(merged[merged['delay_mins'] > 2])
    early_count = len(merged[merged['delay_mins'] < -2])
    ontime_count = len(merged[(merged['delay_mins'] >= -2) & (merged['delay_mins'] <= 2)])
    
    print(f"[Summary Stats]")
    print(f"Total matched vehicles: {len(merged)}")
    print(f"On Time (-2 to 2 mins): {ontime_count} vehicles ({(ontime_count/len(merged))*100:.1f}%)")
    print(f"Delayed (> 2 mins):     {late_count} vehicles ({(late_count/len(merged))*100:.1f}%)")
    print(f"Early   (< -2 mins):    {early_count} vehicles ({(early_count/len(merged))*100:.1f}%)")
    
    print("\n[Live Sample of 15 Random Vehicles]")
    sample = merged.sample(min(15, len(merged)))
    for _, row in sample.iterrows():
        print(f"Route {row['route_id']:>3} | Stop {row['stop_id']:>5} | Sched: {row['arrival_time']:>8} | Actual: {row['actual_time_str']} | {row['Status']}")
        
    print("\n[Exporting Data...]")
    
    # 1. Export to Excel
    export_cols = ['trip_id', 'route_id', 'stop_id', 'arrival_time', 'actual_time_str', 'delay_mins', 'Status']
    merged[export_cols].rename(columns={
        'arrival_time': 'Scheduled_Time',
        'actual_time_str': 'Actual_Time',
        'delay_mins': 'Delay_Minutes'
    }).to_excel('TTC_Delay_Details.xlsx', index=False)
    print("-> Data exported to TTC_Delay_Details.xlsx")
    
    # 2. Export to PDF
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="TTC REAL-TIME DELAY REPORT", ln=1, align='C')
    pdf.cell(200, 10, txt=f"Total matched vehicles: {len(merged)}", ln=1, align='L')
    pdf.cell(200, 10, txt=f"On Time (-2 to 2 mins): {ontime_count} vehicles ({(ontime_count/len(merged))*100:.1f}%)", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Delayed (> 2 mins):     {late_count} vehicles ({(late_count/len(merged))*100:.1f}%)", ln=1, align='L')
    pdf.cell(200, 10, txt=f"Early   (< -2 mins):    {early_count} vehicles ({(early_count/len(merged))*100:.1f}%)", ln=1, align='L')
    
    pdf.cell(200, 10, txt="", ln=1, align='L') # Blank line
    pdf.cell(200, 10, txt="Live Sample of 15 Random Vehicles:", ln=1, align='L')
    
    pdf.set_font("Courier", size=9) # Monospace for the sample
    for _, row in sample.iterrows():
        line = f"Route {row['route_id']:>3} | Stop {row['stop_id']:>5} | Sched: {row['arrival_time']:>8} | Actual: {row['actual_time_str']} | {row['Status']}"
        pdf.cell(200, 5, txt=line, ln=1, align='L')
        
    pdf.output("TTC_RealTime_Report.pdf")
    print("-> Report exported to TTC_RealTime_Report.pdf")

if __name__ == "__main__":
    analyze_realtime()

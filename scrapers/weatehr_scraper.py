import trafilatura
import re
import pandas as pd
from datetime import datetime
import os

# Define file paths using relative directories
OUTPUT_FILE = os.path.join('data', 'raw', 'ranchi_weather_log.csv')
TARGET_URL = 'https://en.tutiempo.net/ranchi.html'

def fetch_weather_text(url):
    """Downloads and extracts raw text from the target URL."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching data from {url}...")
    try:
        downloaded_html = trafilatura.fetch_url(url)
        if downloaded_html:
            return trafilatura.extract(downloaded_html)
        else:
            print("Error: Received empty response.")
            return None
    except Exception as e:
        print(f"Error fetching URL: {e}")
        return None

def parse_weather_data(raw_text):
    """Uses RegEx to extract specific meteorological metrics."""
    extracted_data = {
        "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "wind_speed_kmh": [None],
        "air_pressure_hpa": [None],
        "humidity_percent": [None]
    }

    try:
        wind_match = re.search(r"Wind speed:.*?(\d+)\s*km/h", raw_text)
        pressure_match = re.search(r"Air pressure:.*?(\d+)\s*hPa", raw_text)
        humidity_match = re.search(r"Relative humidity:.*?(\d+)%", raw_text)

        if wind_match: extracted_data["wind_speed_kmh"][0] = int(wind_match.group(1))
        if pressure_match: extracted_data["air_pressure_hpa"][0] = int(pressure_match.group(1))
        if humidity_match: extracted_data["humidity_percent"][0] = int(humidity_match.group(1))
        
        return pd.DataFrame(extracted_data)
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def save_to_csv(df, filepath):
    """Appends the DataFrame to a CSV. Creates headers if the file is new."""
    # Check if the file already exists
    file_exists = os.path.isfile(filepath)
    
    try:
        # mode='a' means append. If file doesn't exist, it creates it.
        df.to_csv(filepath, mode='a', header=not file_exists, index=False)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Successfully logged 1 row to {filepath}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    """Main execution function."""
    raw_text = fetch_weather_text(TARGET_URL)
    
    if raw_text:
        df = parse_weather_data(raw_text)
        if df is not None and not df.isna().all().all(): # Ensure dataframe isn't completely empty
            save_to_csv(df, OUTPUT_FILE)
        else:
            print("Failed to parse meaningful data.")
    else:
        print("Pipeline aborted due to fetch failure.")

if __name__ == "__main__":
    main()

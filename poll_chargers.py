import requests
import pandas as pd
from datetime import datetime
import time

API_URL = "https://api.eptix.co/public/v1/sites/viewport?bLeftLng=-73.60093857164004&bLeftLat=45.520753060328616&uRightLng=-73.58801493440421&uRightLat=45.5275378704352&lng=-73.59447675302243&lat=45.524145567665954&showConstruction=1&hidePartnerNetworkIds=&connectorTypeIds=&siteTagIds="

def fetch_charger_status():
    headers = {
        "Authorization": "Basic OUFHdlg4Mmc1cUt2WWtkNnRuQmpnNTh0Y2o5cXFQaDQ6QTlLdzhoZVlMMmZxVFRWRlRnZnVYdFF1YlVxOU14R1Y=",
        "Referer": "https://lecircuitelectrique.com/",
        "Origin": "https://lecircuitelectrique.com"
    }
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content: {response.content}")
        return None

def save_to_csv(data, filename="charger_status.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, mode='a', header=not pd.io.common.file_exists(filename), index=False)

def main():
    while True:
        data = fetch_charger_status()
        if data:
            timestamp = datetime.now().isoformat()
            processed_data = []
            for charger in data:
                charger_info = {
                    'timestamp': timestamp,
                    'name': charger.get('name'),
                    'status': charger.get('status'),
                    'availableCount': charger.get('stationTypes', [{}])[0].get('availableCount'),
                    'count': charger.get('stationTypes', [{}])[0].get('count')
                }
                processed_data.append(charger_info)
            save_to_csv(processed_data)
        time.sleep(300)  # Wait for 5 minutes

if __name__ == "__main__":
    main()
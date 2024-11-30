import requests
import pandas as pd
from datetime import datetime
import time

API_URL_C = "https://api.eptix.co/public/v1/sites/viewport?bLeftLng=-73.60093857164004&bLeftLat=45.520753060328616&uRightLng=-73.58801493440421&uRightLat=45.5275378704352&lng=-73.59447675302243&lat=45.524145567665954&showConstruction=1&hidePartnerNetworkIds=&connectorTypeIds=&siteTagIds="
API_URL_R = "https://api.eptix.co/public/v1/sites/viewport?bLeftLng=-73.5908332883656&bLeftLat=45.53118088208049&uRightLng=-73.57490848808281&uRightLat=45.53778074840383&lng=-73.58287088822397&lat=45.534480912061014&showConstruction=1&hidePartnerNetworkIds=&connectorTypeIds=&siteTagIds="

def fetch_charger_status(api_url):
    headers = {
        "Authorization": "Basic OUFHdlg4Mmc1cUt2WWtkNnRuQmpnNTh0Y2o5cXFQaDQ6QTlLdzhoZVlMMmZxVFRWRlRnZnVYdFF1YlVxOU14R1Y=",
        "Referer": "https://lecircuitelectrique.com/",
        "Origin": "https://lecircuitelectrique.com"
    }
    response = requests.get(api_url, headers=headers)
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
        for api_url in [API_URL_C, API_URL_R]:
            data = fetch_charger_status(api_url)
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
            time.sleep(60)  # Wait for 1 minute between API calls
        time.sleep(240)  # Wait for 4 minutes before starting the next cycle

if __name__ == "__main__":
    main()
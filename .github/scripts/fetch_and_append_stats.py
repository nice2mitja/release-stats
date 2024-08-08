import requests
import pandas as pd
import os
from datetime import datetime

# GitHub API URL to get releases of the SapMachine repository
api_url = "https://api.github.com/repos/SAP/SapMachine/releases"

# Send a GET request to fetch the releases
response = requests.get(api_url)
releases = response.json()

# Prepare a list to store the data
data = []

# Loop through each release
for release in releases:
    for asset in release['assets']:
        data.append({
            'timestamp': datetime.utcnow().isoformat(),
            'release_name': release['name'],
            'asset_name': asset['name'],
            'download_count': asset['download_count']
        })

# Convert the list to a DataFrame
df = pd.DataFrame(data)

# Define the path to the CSV file
csv_file = 'release_stats.csv'

# Check if the CSV file exists
if os.path.exists(csv_file):
    # If the file exists, append the new data
    df.to_csv(csv_file, mode='a', header=False, index=False)
else:
    # If the file does not exist, create it with headers
    df.to_csv(csv_file, mode='w', header=True, index=False)

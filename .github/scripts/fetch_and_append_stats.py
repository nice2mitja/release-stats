import requests
import pandas as pd
import os
from datetime import datetime, timezone

# GitHub API URL to get releases of the SapMachine repository
api_url = "https://api.github.com/repos/SAP/SapMachine/releases"

# Function to fetch all pages of release data
def fetch_all_releases(api_url):
    releases = []
    while api_url:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        releases.extend(response.json())

        # Check if there's a next page
        api_url = response.links.get('next', {}).get('url')
    return releases

# Fetch all release data
releases = fetch_all_releases(api_url)

# Prepare a list to store the aggregated data
data = []

# Loop through each release to sum up the download counts
for release in releases:
    total_downloads = sum(asset['download_count'] for asset in release['assets'])
    data.append({
        'timestamp': datetime.now(timezone.utc).isoformat(),  # Use timezone-aware datetime
        'release_name': release['name'],
        'total_download_count': total_downloads
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

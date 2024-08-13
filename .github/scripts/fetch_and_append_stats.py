import requests
import pandas as pd
from datetime import datetime
import uuid

# Function to fetch download stats for all releases
def fetch_release_stats():
    releases = []
    url = "https://api.github.com/repos/SAP/SapMachine/releases"
    
    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        releases.extend(data)
        # Get the URL for the next page, if it exists
        url = response.links.get('next', {}).get('url')
    
    stats = []
    for release in releases:
        release_name = release['name']
        release_id = release['id']
        is_prerelease = release['prerelease']  # Check if the release is a pre-release
        total_downloads = sum(asset['download_count'] for asset in release['assets'])
        stats.append({
            'release_name': release_name,
            'release_id': release_id,
            'is_prerelease': is_prerelease,
            'total_downloads': total_downloads
        })
    
    return stats

# Fetch stats and append timestamp
def append_stats_to_csv(stats, file_name="release_stats.csv"):
    unique_id = str(uuid.uuid4())  # Generate a unique ID for the entire run
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')  # Format timestamp as yyyy-mm-dd HH:MM:SS
    data = []
    
    for stat in stats:
        data.append({
            'id': unique_id,  # Use the same unique ID for all rows in this run
            'timestamp': timestamp,
            'release_name': stat['release_name'],
            'release_id': stat['release_id'],
            'is_prerelease': stat['is_prerelease'],
            'total_downloads': stat['total_downloads']
        })
    
    df = pd.DataFrame(data)
    
    # Append to CSV file
    try:
        existing_df = pd.read_csv(file_name)
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        df.to_csv(file_name, index=False)  # Create the file if it doesn't exist
    else:
        df.to_csv(file_name, index=False)

# Main execution
if __name__ == "__main__":
    stats = fetch_release_stats()
    append_stats_to_csv(stats)

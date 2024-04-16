#date.py
#renders index2.html

import requests
import subprocess
import datetime

# Get today's date
today_date = datetime.date.today()
print("Scrapping data for",today_date)
# Calculate yesterday's date
yesterday_date = today_date - datetime.timedelta(days=1)

# Format yesterday's date as 'YYYY-MM-DD'
yesterday_date_str = yesterday_date.isoformat()

# Define the API endpoint URL using yesterday's date
url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={yesterday_date_str}&endDate={yesterday_date_str}'
print ("URL: ", url)
# Make the API request
response = requests.get(url)
 

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()

    game_pks = []
    for date in data['dates']:
        for game in date['games']:
            game_pks.append(game['gamePk'])

    # Print the extracted gamePk values
    print("Extracted gamePk values:")
    print(game_pks)

    # Loop through each gamePk and trigger looperv2.py for each game_id
    for game_id in game_pks:
        print(f"Processing game ID: {game_id}")
        # Trigger looperv2.py script with game_id as argument using subprocess
        subprocess.run(['/usr/bin/python3', '/home/vboxuser/mlb/mlbapi/custompy/looperv2.py', str(game_id)])

else:
    # Print error message if API request fails
    print(f"API request failed with status code: {response.status_code}")

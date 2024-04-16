#games.py
#renders /

import requests
import statsapi
import datetime

# Get the current date in the format 'YYYY-MM-DD'
today_date = datetime.date.today().isoformat()

# Define the API endpoint URL using the current date
url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={today_date}&endDate={today_date}'

def fetch_games_data():
#    url = "http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        data = response.json()
        return data  # Return the JSON data retrieved from the API

    except requests.exceptions.RequestException as e:
        print(f"Error fetching games data: {e}")
        return None
print("Hello, world!")
print (fetch_games_data)
def save_games_data_to_file(data, filename):
    if data:
        try:
            with open(filename, 'w') as file:
                file.write(str(data))  # Write the JSON data to a file
            print(f"Games data saved to {filename}")
        except IOError as e:
            print(f"Error saving games data to file: {e}")

# Uncomment the following lines if you want to execute this script directly
# and save the games data to a file named "games_data.json"
# if __name__ == "__main__":
#     games_data = fetch_games_data()
# 
#     if games_data:
#         save_games_data_to_file(games_data, "games_data.json")

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

try:
    for game_pk in game_pks:
        linescore_data = statsapi.linescore(game_pk)
        print(f"Linescore for gamePk {game_pk}:")
        print(linescore_data)
        print()  # Add a blank line for separation

except Exception as e:
    print(f"Error occurred while fetching linescores: {e}")

else:
    # Print error message if API request fails
    print(f"API request failed with status code: {response.status_code}")


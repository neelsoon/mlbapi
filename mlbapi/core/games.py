import requests

def fetch_games_data():
    url = "http://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        data = response.json()
        return data  # Return the JSON data retrieved from the API

    except requests.exceptions.RequestException as e:
        print(f"Error fetching games data: {e}")
        return None

def save_games_data_to_file(data, filename):
    if data:
        try:
            with open(filename, 'w') as file:
                file.write(str(data))  # Write the JSON data to a file
            print(f"Games data saved to {filename}")
        except IOError as e:
            print(f"Error saving games data to file: {e}")

if __name__ == "__main__":
    games_data = fetch_games_data()

    if games_data:
        save_games_data_to_file(games_data, "games_data.json")
print("Hello, world!")
print (games_data)
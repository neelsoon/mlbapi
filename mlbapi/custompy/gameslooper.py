import requests

def extract_inning_results(game_id):
    # Construct the API endpoint URL for the linescore data of the specified game ID
    api_url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/linescore'

    try:
        # Send GET request to the API endpoint
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Initialize a dictionary to store the inning-by-inning results
            inning_results = {}

            # Extract inning-by-inning results from the response
            innings = data['innings']
            for inning in innings:
                inning_number = inning['num']
                away_team_runs = inning['away'].get('runs', 0)  # Get runs scored by away team (default to 0 if key not found)
                home_team_runs = inning['home'].get('runs', 0)  # Get runs scored by home team (default to 0 if key not found)
                inning_results[inning_number] = {'away': away_team_runs, 'home': home_team_runs}

            return inning_results
        else:
            print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def print_inning_results(inning_results):
    if inning_results is not None:
        # Print the inning-by-inning results
        for inning_number, scores in inning_results.items():
            print(f"Inning {inning_number}: Away Team {scores['away']} - Home Team {scores['home']}")
    else:
        print("No inning-by-inning results retrieved.")

def main():
    game_id = 746655  # Example MLB game ID
    inning_results = extract_inning_results(game_id)

    # Print the inning-by-inning results
    print_inning_results(inning_results)

if __name__ == "__main__":
    main()

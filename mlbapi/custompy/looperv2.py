import requests
import mysql.connector
import sys

def connect_to_mysql(host, username, password, database):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        print("Connected to MySQL database!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

def insert_game_data(connection, game_id, game_date, home_team_id, away_team_id, home_first_inning_score, away_first_inning_score, home_team_name, away_team_name):
    try:
        cursor = connection.cursor()

        # Define the SQL query for inserting game data
        insert_query = """
            INSERT INTO games2024 (gameid, date, hometeamid, awayteamid, hometeam1stinningscore, awayteam1stinningscore, hometeamnicename, awayteamnicename)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the SQL query with the provided data
        cursor.execute(insert_query, (game_id, game_date, home_team_id, away_team_id, home_first_inning_score, away_first_inning_score, home_team_name, away_team_name))

        # Commit the transaction to save changes
        connection.commit()

        print("Game data inserted successfully into the database!")

    except mysql.connector.Error as err:
        print(f"Error inserting game data: {err}")

    finally:
        # Close the cursor
        cursor.close()


def retrieve_game_data(game_id):
    # API endpoint URL for MLB game boxscore
    url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/boxscore'

    try:
        # Send GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract the team names and IDs
            away_team_name = data['teams']['away']['team']['name']
            away_team_id = data['teams']['away']['team']['id']
            home_team_name = data['teams']['home']['team']['name']
            home_team_id = data['teams']['home']['team']['id']

            return data, away_team_name, away_team_id, home_team_name, home_team_id
        else:
            print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
            return None, None, None, None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None, None, None, None

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

def print_inning_results(inning_results, away_team_name, away_team_id, home_team_name, home_team_id):
    if inning_results is not None:
        # Print the inning-by-inning results
        for inning_number, scores in inning_results.items():
            print(f"Inning {inning_number}: {away_team_name} ID: {away_team_id} ({scores['away']}) - {home_team_name} ID: {home_team_id} ({scores['home']})")
    else:
        print("No inning-by-inning results retrieved.")

def print_inning_results_2nd_format(inning_results, away_team_name, home_team_name):
    if inning_results is not None:
        # Extract inning numbers and corresponding scores
        innings = sorted(inning_results.keys())
        away_scores = [inning_results[inning]['away'] for inning in innings]
        home_scores = [inning_results[inning]['home'] for inning in innings]

        # Trim team names to first three letters
        away_team_abbr = away_team_name[:3]
        home_team_abbr = home_team_name[:3]

        # Print the inning numbers
        print(f"Inn:{' '.join(str(inning) for inning in innings)}")

        # Print the away team scores
        print(f"{away_team_abbr} {' '.join(str(score) for score in away_scores)}")

        # Print the home team scores
        print(f"{home_team_abbr} {' '.join(str(score) for score in home_scores)}")
    else:
        print("No inning-by-inning results retrieved.")

def check_first_inning_scores(inning_results, home_team_id, away_team_id):
    if inning_results is not None:
        first_inning = 1
        home_scored_first_inning = inning_results.get(first_inning, {}).get('home', 0) > 0
        away_scored_first_inning = inning_results.get(first_inning, {}).get('away', 0) > 0

        print(f"Home team {home_team_id} scored on 1st inning? {'True' if home_scored_first_inning else 'False'}")
        print(f"Away team {away_team_id} scored on 1st inning? {'True' if away_scored_first_inning else 'False'}")
    else:
        print("No inning-by-inning results retrieved.")

def retrieve_game_date(game_id):
    # API endpoint URL for MLB game content
    url = f'https://statsapi.mlb.com/api/v1/game/{game_id}/content'

    try:
        # Send GET request to the API endpoint
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Extract game date from the JSON data
            if 'media' in data and 'epg' in data['media']:
                epg_items = data['media']['epg']
                for item in epg_items:
                    if 'items' in item:
                        for game in item['items']:
                            if 'gameDate' in game:
                                return game['gameDate']  # Return the game date

        # If game date extraction fails or no valid game date found
        return None

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Request error: {e}")
        return None
    
def main():
        # Check if a game ID is provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <game_id>")
        return

    # Extract the game ID from the command-line argument
    game_id = sys.argv[1]

    # Ensure the game ID is a valid integer
    try:
        game_id = int(game_id)
    except ValueError:
        print("Invalid game ID. Please provide a valid integer game ID.")
        return
    data, away_team_name, away_team_id, home_team_name, home_team_id = retrieve_game_data(game_id)

    if data is not None:
        print(f"Game played between {away_team_name} (Away) ID: {away_team_id} and {home_team_name} (Home) ID: {home_team_id}.")

        # Extract and print inning-by-inning results (traditional format)
        inning_results = extract_inning_results(game_id)
        print_inning_results(inning_results, away_team_name, away_team_id, home_team_name, home_team_id)

        # Extract and print inning-by-inning results (horizontal format)
        print_inning_results_2nd_format(inning_results, away_team_name, home_team_name)

        # Check if either team scored in the first inning
        check_first_inning_scores(inning_results, home_team_id, away_team_id)
        #print game date
        game_date = retrieve_game_date(game_id)
        if game_date:
            print(f"Game date: {game_date}")
        else:
            print("Failed to retrieve game date.")

        # Insert game data into MySQL database
        if inning_results is not None and len(inning_results) > 0:
            first_inning = 1
            home_first_inning_score = inning_results.get(first_inning, {}).get('home', 0)
            away_first_inning_score = inning_results.get(first_inning, {}).get('away', 0)

            # Connect to MySQL
            host = 'localhost'
            username = 'mlbapi'
            password = '123'
            database = 'mlbapi'
            connection = connect_to_mysql(host, username, password, database)

            if connection is not None:
                # Insert game data into the database
                insert_game_data(connection, game_id, game_date, home_team_id, away_team_id, home_first_inning_score, away_first_inning_score, home_team_name, away_team_name)

                # Close the database connection
                connection.close()
                print("MySQL connection closed.")

if __name__ == "__main__":
    main()


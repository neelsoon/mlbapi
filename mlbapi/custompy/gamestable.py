import requests
import statsapi  # Assuming you have imported the statsapi library
import datetime


# Get today's date as a datetime.date object
today_date = datetime.date.today()
print("Today's date: ", today_date)


# Calculate tomorrow's date by adding one day using timedelta
tomorrow_date = today_date + datetime.timedelta(days=1)
print("Tomorrow's date: ", tomorrow_date)


# Calculate yesterday's date by subtracting one day using timedelta
yesterday_date = today_date - datetime.timedelta(days=1)
print("Yesterday's date: ", yesterday_date)


# Define the API endpoint URL using the current date
#url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={today_date}&endDate={today_date}'



def today_mlb_games_view():
    today_game_data_list = []  # List to store extracted game data
    
    # Function to retrieve linescore data for a gamePk
    def get_linescore_data(game_pk):
        try:
            linescore_data = statsapi.linescore(game_pk)
            return linescore_data
        except Exception as e:
            print(f"Error fetching linescore data for gamePk {game_pk}: {e}")
            return None

    # API endpoint URL
 #   url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    todayurl = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={today_date}&endDate={today_date}'
    print(todayurl)

    # Send GET request to fetch data
    response = requests.get(todayurl)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract relevant information from the JSON response
        dates = data["dates"]

        for date in dates:
            games = date["games"]
            for game in games:
                teams = game["teams"]
                away_team = teams["away"]["team"]["name"]
                home_team = teams["home"]["team"]["name"]
                game_date = game["gameDate"]
                venue = game["venue"]["name"]
                game_pk = game["gamePk"]

                # Determine if it's a doubleheader
                double_header = ""
                if game["doubleHeader"] == "S":
                    double_header = " (Game 1 of a doubleheader)"

                # Retrieve linescore data using gamePk
                linescore_data = get_linescore_data(game_pk)
                
                # Prepare game data dictionary
                game_data = {
                    "away_team": away_team,
                    "home_team": home_team,
                    "game_date": game_date,
                    "venue": venue,
                    "double_header": double_header,
                    "linescore_data": linescore_data  # Include linescore data
                }
                
                # Append game data to the list
                today_game_data_list.append(game_data)
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return today_game_data_list

# Example usage:
if __name__ == "__main__":
    todays_games = today_mlb_games_view()
    for game in todays_games:
        print(f"{game['away_team']} vs. {game['home_team']}{game['double_header']}")
        print(f"Date: {game['game_date']}")
        print(f"Venue: {game['venue']}")
        if game['linescore_data']:
            print("")
            print(f" {game['linescore_data']}")
        else:
            print("Failed to retrieve linescore data")
        print("======================")

#yesterday game datacode block
def yesterday_mlb_games_view():
    yesterday_game_data_list = []  # List to store extracted game data
    
    # Function to retrieve linescore data for a gamePk
    def get_linescore_data(game_pk):
        try:
            linescore_data = statsapi.linescore(game_pk)
            return linescore_data
        except Exception as e:
            print(f"Error fetching linescore data for gamePk {game_pk}: {e}")
            return None

    # Get yesterday's date
    yesterday_date = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={yesterday_date}&endDate={yesterday_date}'
    
    print(yesterday_url)

    # Send GET request to fetch data
    response = requests.get(yesterday_url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract relevant information from the JSON response
        dates = data["dates"]

        for date in dates:
            games = date["games"]
            for game in games:
                teams = game["teams"]
                away_team = teams["away"]["team"]["name"]
                home_team = teams["home"]["team"]["name"]
                game_date = game["gameDate"]
                venue = game["venue"]["name"]
                game_pk = game["gamePk"]

                # Determine if it's a doubleheader
                double_header = ""
                if game["doubleHeader"] == "S":
                    double_header = " (Game 1 of a doubleheader)"

                # Retrieve linescore data using gamePk
                linescore_data = get_linescore_data(game_pk)
                
                # Prepare game data dictionary
                game_data = {
                    "away_team": away_team,
                    "home_team": home_team,
                    "game_date": game_date,
                    "venue": venue,
                    "double_header": double_header,
                    "linescore_data": linescore_data  # Include linescore data
                }
                
                # Append game data to the list
                yesterday_game_data_list.append(game_data)
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return yesterday_game_data_list

# Example usage:
if __name__ == "__main__":
    yesterdays_games = yesterday_mlb_games_view()
    for game in yesterdays_games:
        print("Will now print yesterday games")
        print(f"{game['away_team']} vs. {game['home_team']}{game['double_header']}")
        print(f"Date: {game['game_date']}")
        print(f"Venue: {game['venue']}")
        if game['linescore_data']:
            print("")
            print(f" {game['linescore_data']}")
        else:
            print("Failed to retrieve linescore data")
        print("======================")



#tomorrow game datacode block
def tomorrow_mlb_games_view():
    tomorrow_game_data_list = []  # List to store extracted game data
    
    # Function to retrieve linescore data for a gamePk
    def get_linescore_data(game_pk):
        try:
            linescore_data = statsapi.linescore(game_pk)
            return linescore_data
        except Exception as e:
            print(f"Error fetching linescore data for gamePk {game_pk}: {e}")
            return None

    # Get tomorrow's date
    tomorrow_date = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_url = f'https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate={tomorrow_date}&endDate={tomorrow_date}'
    
    print(tomorrow_url)

    # Send GET request to fetch data
    response = requests.get(tomorrow_url)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Extract relevant information from the JSON response
        dates = data["dates"]

        for date in dates:
            games = date["games"]
            for game in games:
                teams = game["teams"]
                away_team = teams["away"]["team"]["name"]
                home_team = teams["home"]["team"]["name"]
                game_date = game["gameDate"]
                venue = game["venue"]["name"]
                game_pk = game["gamePk"]

                # Determine if it's a doubleheader
                double_header = ""
                if game["doubleHeader"] == "S":
                    double_header = " (Game 1 of a doubleheader)"

                # Retrieve linescore data using gamePk
                linescore_data = get_linescore_data(game_pk)
                
                # Prepare game data dictionary
                game_data = {
                    "away_team": away_team,
                    "home_team": home_team,
                    "game_date": game_date,
                    "venue": venue,
                    "double_header": double_header,
                    "linescore_data": linescore_data  # Include linescore data
                }
                
                # Append game data to the list
                tomorrow_game_data_list.append(game_data)
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return tomorrow_game_data_list

# Example usage:
if __name__ == "__main__":
    tomorrows_games = tomorrow_mlb_games_view()
    for game in tomorrows_games:
        print("Will now print tomorrow games")
        print(f"{game['away_team']} vs. {game['home_team']}{game['double_header']}")
        print(f"Date: {game['game_date']}")
        print(f"Venue: {game['venue']}")
        if game['linescore_data']:
            print("")
            print(f" {game['linescore_data']}")
        else:
            print("Failed to retrieve linescore data")
        print("======================")
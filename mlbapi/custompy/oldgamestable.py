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



def mlb_games_view():
    game_data_list = []  # List to store extracted game data
    
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
                game_data_list.append(game_data)
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
    
    return game_data_list

# Example usage:
if __name__ == "__main__":
    games = mlb_games_view()
    for game in games:
        print(f"{game['away_team']} vs. {game['home_team']}{game['double_header']}")
        print(f"Date: {game['game_date']}")
        print(f"Venue: {game['venue']}")
        if game['linescore_data']:
            print("")
            print(f" {game['linescore_data']}")
        else:
            print("Failed to retrieve linescore data")
        print("======================")

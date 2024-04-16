#vies.py
from django.shortcuts import render
from custompy.games import fetch_games_data
from custompy.dbconn import (
    fetch_noruns_data,
    fetch_noruns_data_10_days,
    fetch_noruns_data_3_days
) # Import fetch_noruns_data from dbconn.py
#from custompy.gamestable import mlb_games_view as today_mlb_games_data
from custompy.gamestable import today_mlb_games_view as today_mlb_games_data # Import mlb_games_view function from gamestable.py
from custompy.gamestable import yesterday_mlb_games_view as yesterday_mlb_games_data
from custompy.gamestable import tomorrow_mlb_games_view as tomorrow_mlb_games_data

from django.http import JsonResponse
import subprocess

# Create your views here.
#def index(request):
#    return render(request, 'index.html')

def index(request):
    # Call today's mlb_games_view to retrieve MLB game data for today
    today_games = today_mlb_games_data()

    # Call yesterday's mlb_games_view to retrieve MLB game data for yesterday
    yesterday_games = yesterday_mlb_games_data()

        # Call tomorrow's mlb_games_view to retrieve MLB game data for tomorrow
    tomorrow_games = tomorrow_mlb_games_data()

    # Prepare today's game data for rendering in the template
    today_games_data = []
    for game in today_games:
        game_info = {
            'away_team': game['away_team'],
            'home_team': game['home_team'],
            'game_date': game['game_date'],
            'venue': game['venue'],
            'double_header': game['double_header'],
            'linescore_data': game['linescore_data'] if game['linescore_data'] else None
        }
        today_games_data.append(game_info)

    # Prepare yesterday's game data for rendering in the template
    yesterday_games_data = []
    for game in yesterday_games:
        game_info = {
            'away_team': game['away_team'],
            'home_team': game['home_team'],
            'game_date': game['game_date'],
            'venue': game['venue'],
            'double_header': game['double_header'],
            'linescore_data': game['linescore_data'] if game['linescore_data'] else None
        }
        yesterday_games_data.append(game_info)


        # Starts Prepare tomorrow's game data for rendering in the template
    tomorrow_games_data = []
    for game in tomorrow_games:
        game_info = {
            'away_team': game['away_team'],
            'home_team': game['home_team'],
            'game_date': game['game_date'],
            'venue': game['venue'],
            'double_header': game['double_header'],
            'linescore_data': game['linescore_data'] if game['linescore_data'] else None
        }
        tomorrow_games_data.append(game_info)
 # ENDS Prepare tomorrow's game data for rendering in the template

    context = {
        'today_games_data': today_games_data,  # Pass today's MLB game data to the template context
        'yesterday_games_data': yesterday_games_data,  # Pass yesterday's MLB game data to the template context
        'tomorrow_games_data': tomorrow_games_data  # Pass yesterday's MLB game data to the template context
    }
    return render(request, 'index.html', context)




def noruntable(request):
    # Call fetch_noruns_data to get the data for all games
    noruns_data = fetch_noruns_data()

    # Call fetch_noruns_data_10_days to get the data for the last 10 days
    noruns_data_10_days = fetch_noruns_data_10_days()

    # Call fetch_noruns_data_3_days to get the data for the last 3 days
    noruns_data_3_days = fetch_noruns_data_3_days()

    # Prepare the context dictionary with all fetched data
    context = {
        'noruns_data': noruns_data,
        'noruns_data_10_days': noruns_data_10_days,
        'noruns_data_3_days': noruns_data_3_days
    }

    # Render the noruntable.html template with the context
    return render(request, 'noruntable.html', context)





def mlb_games_view(request):
    # Call mlb_games_view (from gamestable.py) to retrieve MLB game data
    games = today_mlb_games_data()

    # Prepare game data for rendering in the template
    games_data = []
    for game in games:
        game_info = {
            'away_team': game['away_team'],
            'home_team': game['home_team'],
            'game_date': game['game_date'],
            'venue': game['venue'],
            'double_header': game['double_header'],
            'linescore_data': game['linescore_data'] if game['linescore_data'] else None
        }
        games_data.append(game_info)

    context = {
        'games_data': games_data  # Pass the MLB game data to the template context
    }
    return render(request, 'index2.html', context)




def run_date_script(request):
    if request.method == 'GET':
        date = request.GET.get('date', None)

        if date:
            try:
                # Define the command to execute date.py script with the specified date
                command = ['python', '/home/vboxuser/mlb/mlbapi/custompy/date.py']
                
                # Append the date parameter to the command
                command.append(date)

                # Execute the command using subprocess
                subprocess.run(command, check=True)
                
                return JsonResponse({'message': 'Script executed successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'error': 'Date parameter missing'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

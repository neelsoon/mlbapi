import mysql.connector

def fetch_noruns_data():
    try:
        # Database connection parameters
        db_config = {
            'host': 'localhost',
            'user': 'mlbapi',
            'password': '123',
            'database': 'mlbapi'
        }

        # Establish a connection to the MariaDB server
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print('Connected to MariaDB server')

            # Execute SQL query to fetch noruns data
            cursor = connection.cursor()

            # Updated SQL query with the new query you provided
            sql_query = """
            SELECT
                teamid,
                teamname,
                COUNT(DISTINCT gameid) AS total_games_played,
                SUM(home_no_runs) AS total_home_no_runs_1st_inning,
                SUM(away_no_runs) AS total_away_no_runs_1st_inning,
                SUM(home_no_runs + away_no_runs) AS total_no_runs_1st_inning,
                (SUM(home_no_runs + away_no_runs) / COUNT(DISTINCT gameid)) * 100 AS no_1st_inning_percentage
            FROM (
                SELECT
                    hometeamid AS teamid,
                    hometeamnicename AS teamname,
                    gameid,
                    CASE WHEN hometeam1stinningscore = 0 THEN 1 ELSE 0 END AS home_no_runs,
                    0 AS away_no_runs
                FROM
                    games2024
                UNION ALL
                SELECT
                    awayteamid AS teamid,
                    awayteamnicename AS teamname,
                    gameid,
                    0 AS home_no_runs,
                    CASE WHEN awayteam1stinningscore = 0 THEN 1 ELSE 0 END AS away_no_runs
                FROM
                    games2024
            ) AS combined
            GROUP BY
                teamid, teamname
            ORDER BY
                no_1st_inning_percentage DESC;
            """

            cursor.execute(sql_query)
            noruns_data = cursor.fetchall()

            # Print the SQL results
            print("SQL Results:")
            for row in noruns_data:
                print(row)

            # Close cursor and connection
            cursor.close()
            connection.close()
            print('Connection to MariaDB server closed')

            return noruns_data

    except mysql.connector.Error as error:
        print(f'Error connecting to MariaDB: {error}')
        return None

# Call the function to fetch and print the results
noruns_data = fetch_noruns_data()


import mysql.connector

def fetch_noruns_data_10_days():
    try:
        # Database connection parameters
        db_config = {
            'host': 'localhost',
            'user': 'mlbapi',
            'password': '123',
            'database': 'mlbapi'
        }

        # Establish a connection to the MariaDB server
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print('Connected to MariaDB server')

            # Execute SQL query to fetch noruns data for the last 10 days
            cursor = connection.cursor()

            # SQL query with date filter for the last 10 days
            sql_query = """
            SELECT
                teamid,
                teamname,
                COUNT(DISTINCT gameid) AS total_games_played,
                SUM(home_no_runs) AS total_home_no_runs_1st_inning,
                SUM(away_no_runs) AS total_away_no_runs_1st_inning,
                SUM(home_no_runs + away_no_runs) AS total_no_runs_1st_inning,
                (SUM(home_no_runs + away_no_runs) / COUNT(DISTINCT gameid)) * 100 AS no_1st_inning_percentage
            FROM (
                SELECT
                    hometeamid AS teamid,
                    hometeamnicename AS teamname,
                    gameid,
                    CASE WHEN hometeam1stinningscore = 0 THEN 1 ELSE 0 END AS home_no_runs,
                    0 AS away_no_runs
                FROM
                    games2024
                WHERE
                    date >= CURDATE() - INTERVAL 10 DAY  -- Filter games from the last 10 days
                UNION ALL
                SELECT
                    awayteamid AS teamid,
                    awayteamnicename AS teamname,
                    gameid,
                    0 AS home_no_runs,
                    CASE WHEN awayteam1stinningscore = 0 THEN 1 ELSE 0 END AS away_no_runs
                FROM
                    games2024
                WHERE
                    date >= CURDATE() - INTERVAL 10 DAY  -- Filter games from the last 10 days
            ) AS combined
            GROUP BY
                teamid, teamname
            ORDER BY
                no_1st_inning_percentage DESC;
            """

            cursor.execute(sql_query)
            noruns_data_10_days = cursor.fetchall()

            # Print the SQL results for the last 10 days
            print("SQL Results for the last 10 days:")
            for row in noruns_data_10_days:
                print(row)

            # Close cursor and connection
            cursor.close()
            connection.close()
            print('Connection to MariaDB server closed')

            return noruns_data_10_days

    except mysql.connector.Error as error:
        print(f'Error connecting to MariaDB: {error}')
        return None

# Call the function to fetch and print the results for the last 10 days
noruns_data_10_days = fetch_noruns_data_10_days()

import mysql.connector

def fetch_noruns_data_3_days():
    try:
        # Database connection parameters
        db_config = {
            'host': 'localhost',
            'user': 'mlbapi',
            'password': '123',
            'database': 'mlbapi'
        }

        # Establish a connection to the MariaDB server
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            print('Connected to MariaDB server')

            # Execute SQL query to fetch noruns data for the last 3 days
            cursor = connection.cursor()

            # SQL query with date filter for the last 3 days
            sql_query = """
            SELECT
                teamid,
                teamname,
                COUNT(DISTINCT gameid) AS total_games_played,
                SUM(home_no_runs) AS total_home_no_runs_1st_inning,
                SUM(away_no_runs) AS total_away_no_runs_1st_inning,
                SUM(home_no_runs + away_no_runs) AS total_no_runs_1st_inning,
                (SUM(home_no_runs + away_no_runs) / COUNT(DISTINCT gameid)) * 100 AS no_1st_inning_percentage
            FROM (
                SELECT
                    hometeamid AS teamid,
                    hometeamnicename AS teamname,
                    gameid,
                    CASE WHEN hometeam1stinningscore = 0 THEN 1 ELSE 0 END AS home_no_runs,
                    0 AS away_no_runs
                FROM
                    games2024
                WHERE
                    date >= CURDATE() - INTERVAL 3 DAY  -- Filter games from the last 3 days
                UNION ALL
                SELECT
                    awayteamid AS teamid,
                    awayteamnicename AS teamname,
                    gameid,
                    0 AS home_no_runs,
                    CASE WHEN awayteam1stinningscore = 0 THEN 1 ELSE 0 END AS away_no_runs
                FROM
                    games2024
                WHERE
                    date >= CURDATE() - INTERVAL 3 DAY  -- Filter games from the last 3 days
            ) AS combined
            GROUP BY
                teamid, teamname
            ORDER BY
                no_1st_inning_percentage DESC;
            """

            cursor.execute(sql_query)
            noruns_data_3_days = cursor.fetchall()

            # Print the SQL results for the last 3 days
            print("SQL Results for the last 3 days:")
            for row in noruns_data_3_days:
                print(row)

            # Close cursor and connection
            cursor.close()
            connection.close()
            print('Connection to MariaDB server closed')

            return noruns_data_3_days

    except mysql.connector.Error as error:
        print(f'Error connecting to MariaDB: {error}')
        return None

# Call the function to fetch and print the results for the last 3 days
noruns_data_3_days = fetch_noruns_data_3_days()

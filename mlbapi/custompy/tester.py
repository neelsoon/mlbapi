#dbconn.py
# dbconn.py

import mysql.connector

def connect_to_mariadb():
    try:
        # Database connection parameters (replace with your actual credentials)
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

            # Execute SQL query to fetch aggregated data
            fetch_and_print_aggregated_data(connection)

            # Close connection
            connection.close()
            print('Connection to MariaDB server closed')

    except mysql.connector.Error as error:
        print(f'Error connecting to MariaDB: {error}')

def fetch_and_print_aggregated_data(connection):
    try:
        # Define the SQL query for fetching aggregated data
        sql_query = """
            SELECT
                teamid,
                teamname,
                SUM(norun1stashomeclub) AS total_home_no_runs_1st_inning,
                SUM(awaynoruns1stinning) AS total_away_no_runs_1st_inning,
                SUM(norun1stashomeclub + awaynoruns1stinning) AS total_no_runs_1st_inning
            FROM (
                SELECT
                    hometeamid AS teamid,
                    hometeamnicename AS teamname,
                    COUNT(*) AS norun1stashomeclub,
                    0 AS awaynoruns1stinning
                FROM
                    games2024
                WHERE
                    hometeam1stinningscore = 0
                GROUP BY
                    hometeamid, hometeamnicename

                UNION ALL

                SELECT
                    awayteamid AS teamid,
                    awayteamnicename AS teamname,
                    0 AS norun1stashomeclub,
                    COUNT(*) AS awaynoruns1stinning
                FROM
                    games2024
                WHERE
                    awayteam1stinningscore = 0
                GROUP BY
                    awayteamid, awayteamnicename
            ) AS combined
            GROUP BY
                teamid, teamname
            ORDER BY
                total_no_runs_1st_inning DESC;
        """

        # Create a cursor and execute the SQL query
        cursor = connection.cursor()
        cursor.execute(sql_query)
        

        # Fetch all rows and print the results
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        # Close cursor
        cursor.close()
        fetch_noruns_data = rows
        return fetch_noruns_data 
        

    except mysql.connector.Error as error:
        print(f'Error executing SQL query: {error}')

# Entry point to connect to MariaDB and fetch data
if __name__ == '__main__':
    connect_to_mariadb()

# dbconn.py

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
            sql_query = """
            SELECT
                teamid,
                teamname,
                SUM(norun1stashomeclub) AS total_home_no_runs_1st_inning,
                SUM(awaynoruns1stinning) AS total_away_no_runs_1st_inning,
                SUM(norun1stashomeclub + awaynoruns1stinning) AS total_no_runs_1st_inning
            FROM (
                SELECT
                    hometeamid AS teamid,
                    hometeamnicename AS teamname,
                    COUNT(*) AS norun1stashomeclub,
                    0 AS awaynoruns1stinning
                FROM
                    games2024
                WHERE
                    hometeam1stinningscore = 0
                GROUP BY
                    hometeamid, hometeamnicename

                UNION ALL

                SELECT
                    awayteamid AS teamid,
                    awayteamnicename AS teamname,
                    0 AS norun1stashomeclub,
                    COUNT(*) AS awaynoruns1stinning
                FROM
                    games2024
                WHERE
                    awayteam1stinningscore = 0
                GROUP BY
                    awayteamid, awayteamnicename
            ) AS combined
            GROUP BY
                teamid, teamname
            ORDER BY
                total_no_runs_1st_inning DESC;
        """

            cursor.execute(sql_query)
            noruns_data = cursor.fetchall()

            # Close cursor and connection
            cursor.close()
            connection.close()
            print('Connection to MariaDB server closed')

            return noruns_data

    except mysql.connector.Error as error:
        print(f'Error connecting to MariaDB: {error}')
        return None

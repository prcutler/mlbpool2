import pendulum
import requests
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory
import mlbpool.data.config as config


class GameDayService:

    @staticmethod
    def get_season_opener_date():

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        all_star_game_date = session.query(SeasonInfo.all_star_game_date)
        tz = pendulum.timezone('America/New_York')

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/full_game_schedule.json',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        gameday_json = response.json()
        gameday_data = gameday_json["fullgameschedule"]["gameentry"][0]

        """Get the date of the season opener"""

        for gameday_info in gameday_data:
            first_game_date = gameday_data["date"]

            return first_game_date

    @staticmethod
    def get_season_opener_time():
        """Get the timeof the season opener's game"""

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        all_star_game_date = session.query(SeasonInfo.all_star_game_date)
        tz = pendulum.timezone('America/New_York')

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/full_game_schedule.json',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        gameday_json = response.json()
        gameday_data = gameday_json["fullgameschedule"]["gameentry"][0]

        for gameday_info in gameday_data:
            first_game_time = gameday_data["time"]

            return first_game_time

    @staticmethod
    def get_season_opener_teams():
        """Get the teams playing in the season opener"""

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        all_star_game_date = session.query(SeasonInfo.all_star_game_date)
        tz = pendulum.timezone('America/New_York')

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/full_game_schedule.json',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        gameday_json = response.json()
        gameday_data = gameday_json["fullgameschedule"]["gameentry"][0]

        for gameday_info in gameday_data:
            away_team = gameday_data["awayTeam"]["Name"]
            home_team = gameday_data["homeTeam"]["Name"]

            season_opener_teams = [away_team, home_team]

            return season_opener_teams

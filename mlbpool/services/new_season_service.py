from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory
import requests
from requests.auth import HTTPBasicAuth
import mlbpool.data.config as config
import pendulum
import pymysql

# Needed for pymysql to understand Pendulum datetimes
pymysql.converters.conversions[pendulum.DateTime] = pymysql.converters.escape_datetime


class NewSeasonService:
    @staticmethod
    def get_install():
        return []

    # TODO Add logging
    @classmethod
    def create_season(cls, season, all_star_game_date):
        """After first time installation or before a new season starts, this will update the season year
            in the database.  This is used to for the MySportsFeeds API to get the correct year of stats needed."""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo)

        new_season = SeasonInfo()
        new_season.current_season = season

        all_star_game_datetime = pendulum.parse(all_star_game_date)

        new_season.all_star_game_date = all_star_game_date

        if season_row.count() == 0:
            print("New install, adding a season")

            response = requests.get('https://api.mysportsfeeds.com/v2.0/pull/mlb/' + str(season) +
                                    '-regular/games.json',
                                    auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw))

            gameday_json = response.json()
            gameday_data = gameday_json["games"][0]
            last_game_data = gameday_json["games"][-1]

            first_game_date = gameday_data["schedule"]["startTime"]

            season_start_utc = pendulum.parse(first_game_date, tz='UTC')
            season_start_date = season_start_utc.in_tz('America/New_York')
            first_game_time = season_start_date.to_time_string()

            away_team = gameday_data["schedule"]["awayTeam"]["abbreviation"]
            home_team = gameday_data["schedule"]["homeTeam"]["abbreviation"]
            last_game_date = last_game_data["schedule"]["startTime"]
            last_game_utc = pendulum.parse(last_game_date, tz='UTC')
            last_game_datetime = last_game_utc.in_tz('America/New_York')

            new_season = SeasonInfo(season_start_date=season_start_date, season_start_time=first_game_time,
                                    home_team=home_team, away_team=away_team, current_season=season,
                                    all_star_game_date=all_star_game_datetime, season_end_date=last_game_datetime)

            # TODO Add log for new_season

            session.add(new_season)
            session.commit()
            session.close()

        else:
            print("Existing season found, updating to new year")

            response = requests.get('https://api.mysportsfeeds.com/v2.0/pull/mlb/' + str(season) +
                                    '-regular/games.json',
                                    auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw))

            gameday_json = response.json()
            gameday_data = gameday_json["games"][0]
            last_game_data = gameday_json["games"][-1]

            first_game_date = gameday_data["schedule"]["startTime"]

            season_start_utc = pendulum.parse(first_game_date, tz='UTC')
            season_start_date = season_start_utc.in_tz('America/New_York')
            first_game_time = season_start_date.to_time_string()

            away_team = gameday_data["schedule"]["awayTeam"]["abbreviation"]
            home_team = gameday_data["schedule"]["homeTeam"]["abbreviation"]
            last_game_date = last_game_data["schedule"]["startTime"]
            last_game_utc = pendulum.parse(last_game_date, tz='UTC')
            last_game_datetime = last_game_utc.in_tz('America/New_York')

            update_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
            update_row.current_season = season
            update_row.season_start_date = season_start_date
            update_row.all_star_game_date = all_star_game_date
            update_row.season_start_time = first_game_time
            update_row.away_team = away_team
            update_row.home_team = home_team
            update_row.season_end_date = last_game_datetime

            # TODO Add log for new season

            session.commit()
            session.close()

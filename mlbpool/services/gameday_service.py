import pendulum
import requests
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory
import mlbpool.data.config as config
from dateutil import parser


class GameDayService:

    @staticmethod
    def get_season_opener_date():

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)

    @staticmethod
    def get_season_opener_time(get_days, get_hours, get_minutes):
        """Get the time of the season opener's game"""

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        season_opener_time = session.query(SeasonInfo.season_start_time)

        tz = pendulum.timezone('America/New_York')
        season_start_dt = season_opener_date + "T" + season_opener_time[:-2]
        now = pendulum.now(tz=tz)
        delta = season_start_dt - now
        delta.days = get_days
        delta.hours = get_hours
        delta.minutes = get_minutes




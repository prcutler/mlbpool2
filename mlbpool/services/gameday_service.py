import pendulum
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory


class GamedayService:

    @staticmethod
    def get_season_opener_date:
        """Get the date of the season opener"""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        all_star_game_date = session.query(SeasonInfo.all_star_game_date)
        tz = pendulum.timezone('America/New_York')
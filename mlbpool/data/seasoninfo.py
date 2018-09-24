from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class SeasonInfo(SqlAlchemyBase):
    __tablename__ = 'SeasonInfo'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    current_season = sqlalchemy.Column(sqlalchemy.Integer)
    season_start_date = sqlalchemy.Column(sqlalchemy.DateTime)
    season_start_time = sqlalchemy.Column(sqlalchemy.String(10))
    home_team = sqlalchemy.Column(sqlalchemy.String(16))
    away_team = sqlalchemy.Column(sqlalchemy.String(16))
    all_star_game_date = sqlalchemy.Column(sqlalchemy.DateTime)
    season_end_date = sqlalchemy.Column(sqlalchemy.DateTime)

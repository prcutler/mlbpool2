from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class MLBSchedule(SqlAlchemyBase):
    __tablename__ = 'MLBSchedule'
    game_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    game_date = sqlalchemy.Column(sqlalchemy.String(32), index=True)
    away_team = sqlalchemy.Column(sqlalchemy.Integer)
    home_team = sqlalchemy.Column(sqlalchemy.Integer)
    season = sqlalchemy.Column(sqlalchemy.Integer)

from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


# Store pre interleague trade individual MLB Player stats in this table
class InterleagueTrades(SqlAlchemyBase):
    __tablename__ = "InterleagueTrades"
    primary_key = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    season = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    update_date = sqlalchemy.Column(sqlalchemy.DATETIME, index=True)
    player_id = sqlalchemy.Column(sqlalchemy.Integer)
    home_runs = sqlalchemy.Column(sqlalchemy.Integer)
    batting_average = sqlalchemy.Column(sqlalchemy.Float)
    at_bats = sqlalchemy.Column(sqlalchemy.Integer)
    hits = sqlalchemy.Column(sqlalchemy.Integer)
    plate_appearances = sqlalchemy.Column(sqlalchemy.Float)
    player_games_played = sqlalchemy.Column(sqlalchemy.Float)
    RBI = sqlalchemy.Column(sqlalchemy.Integer)
    pitcher_wins = sqlalchemy.Column(sqlalchemy.Float)
    ERA = sqlalchemy.Column(sqlalchemy.Float)
    earned_runs = sqlalchemy.Column(sqlalchemy.Integer)
    innings_pitched = sqlalchemy.Column(sqlalchemy.Float)

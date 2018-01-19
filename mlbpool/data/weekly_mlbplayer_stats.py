from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


# Store all individual MLB Player stats in this table
class WeeklyMLBPlayerStats(SqlAlchemyBase):
    __tablename__ = 'WeeklyMLBPlayerStats'
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    week = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    player_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ActiveMLBPlayers.player_id'))
    passyds = sqlalchemy.Column(sqlalchemy.Integer)
    rushyds = sqlalchemy.Column(sqlalchemy.Integer)
    recyds = sqlalchemy.Column(sqlalchemy.Integer)
    sacks = sqlalchemy.Column(sqlalchemy.REAL)
    interceptions = sqlalchemy.Column(sqlalchemy.Integer)

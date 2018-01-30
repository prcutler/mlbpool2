from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class ActiveMLBPlayers(SqlAlchemyBase):
    __tablename__ = 'ActiveMLBPlayers'
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True)
    season = sqlalchemy.Column(sqlalchemy.Integer)
    team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('TeamInfo.team_id'))
    firstname = sqlalchemy.Column(sqlalchemy.String(16))
    lastname = sqlalchemy.Column(sqlalchemy.String(32))
    position = sqlalchemy.Column(sqlalchemy.String(8), index=True)
    player_id = sqlalchemy.Column(sqlalchemy.Integer, index=True)



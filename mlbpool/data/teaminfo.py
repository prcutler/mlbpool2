from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class TeamInfo(SqlAlchemyBase):
    __tablename__ = "TeamInfo"
    team_id = sqlalchemy.Column(sqlalchemy.Integer, index=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(16))
    city = sqlalchemy.Column(sqlalchemy.String(32))
    team_abbr = sqlalchemy.Column(sqlalchemy.String(16))
    league_id = sqlalchemy.Column(sqlalchemy.Integer)
    division_id = sqlalchemy.Column(sqlalchemy.Integer)

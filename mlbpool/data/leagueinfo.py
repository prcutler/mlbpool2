from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


# Point values for each category
class LeagueInfo(SqlAlchemyBase):
    __tablename__ = 'LeagueInfo'
    league_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    league = sqlalchemy.Column(sqlalchemy.String(8))

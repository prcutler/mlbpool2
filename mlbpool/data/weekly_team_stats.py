from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


# Store all individual NFL Player stats in this table
class WeeklyTeamStats(SqlAlchemyBase):
    __tablename__ = 'WeeklyTeamStats'
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    update_date = sqlalchemy.Column(sqlalchemy.Date, index=True)
    team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('TeamInfo.team_id'))
    division_rank = sqlalchemy.Column(sqlalchemy.Integer)
    league_rank = sqlalchemy.Column(sqlalchemy.Integer)
    team_wins = sqlalchemy.Column(sqlalchemy.Integer)
    tiebreaker_twin_wins = sqlalchemy.Column(sqlalchemy.Integer)

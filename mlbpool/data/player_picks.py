from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class PlayerPicks(SqlAlchemyBase):
    __tablename__ = 'PlayerPicks'
    pick_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.String(32), sqlalchemy.ForeignKey('Account.id'))
    season = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    date_submitted = sqlalchemy.Column(sqlalchemy.DATETIME)
    league_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('LeagueInfo.league_id'))
    division_id = sqlalchemy.Column(sqlalchemy.Integer)
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('TeamInfo.team_id'))
    multiplier = sqlalchemy.Column(sqlalchemy.Float, default=1)
    player_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ActiveMLBPlayers.player_id'))
    pick_type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('PickTypes.pick_type_id'))
    twins_wins = sqlalchemy.Column(sqlalchemy.Integer)

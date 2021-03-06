from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


class WeeklyPlayerResults(SqlAlchemyBase):
    __tablename__ = "WeeklyPlayerResults"
    primary_key = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True
    )
    pick_id = sqlalchemy.Column(sqlalchemy.Integer, index=True)
    season = sqlalchemy.Column(sqlalchemy.Integer)
    update_date = sqlalchemy.Column(sqlalchemy.DATE)
    points_earned = sqlalchemy.Column(sqlalchemy.Float)

from mlbpool.data.modelbase import SqlAlchemyBase
import sqlalchemy


# Point values for each category
class PickTypePoints(SqlAlchemyBase):
    __tablename__ = 'PickTypePoints'
    primary_key = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    pick_type_id = sqlalchemy.Column(sqlalchemy.Integer)
    rank = sqlalchemy.Column(sqlalchemy.Integer)
    points = sqlalchemy.Column(sqlalchemy.Float)

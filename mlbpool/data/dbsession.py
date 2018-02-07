import sqlalchemy
import sqlalchemy.orm
import mlbpool.data.config as config
from mlbpool.data.modelbase import SqlAlchemyBase
# noinspection PyUnresolvedReferences
import mlbpool.data.account
# noinspection PyUnresolvedReferences
import mlbpool.data.activeplayers
# noinspection PyUnresolvedReferences
import mlbpool.data.seasoninfo
# noinspection PyUnresolvedReferences
import mlbpool.data.player_picks
# noinspection PyUnresolvedReferences
import mlbpool.data.teaminfo
# noinspection PyUnresolvedReferences
import mlbpool.data.passwordreset
# noinspection PyUnresolvedReferences
import mlbpool.data.picktypes
# noinspection PyUnresolvedReferences
import mlbpool.data.leagueinfo
# noinspection PyUnresolvedReferences
import mlbpool.data.divisioninfo
# noinspection PyUnresolvedReferences
import mlbpool.data.pick_type_points
# noinspection PyUnresolvedReferences
import mlbpool.data.picktypes
from sqlalchemy.pool import NullPool


class DbSessionFactory:
    factory = None

    # Start a database session at app startup
    @staticmethod
    def global_init():
 #       if DbSessionFactory.factory:
 #           return

 #       if not db_file or not db_file.strip():
 #           raise Exception("You must specify a data file.")

        conn_str = 'mysql+pymysql://' + config.db_user + ':' + config.db_pw + '@localhost/mlbpooldb'
        print("Connecting to db with conn string: {}".format(conn_str))

        engine = sqlalchemy.create_engine(conn_str, poolclass=NullPool, echo=False)

        SqlAlchemyBase.metadata.create_all(engine)
        DbSessionFactory.factory = sqlalchemy.orm.sessionmaker(bind=engine)

    @staticmethod
    def create_session():
        return DbSessionFactory.factory()

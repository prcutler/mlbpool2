import sqlalchemy
import sqlalchemy.orm
from mlbpool.data.modelbase import SqlAlchemyBase
# noinspection PyUnresolvedReferences
# import mlbpool.data.account
# noinspection PyUnresolvedReferences
# import mlbpool.data.activeplayers
# noinspection PyUnresolvedReferences
# import mlbpool.data.seasoninfo
# noinspection PyUnresolvedReferences
# import mlbpool.data.player_picks
# noinspection PyUnresolvedReferences
# import mlbpool.data.points
# noinspection PyUnresolvedReferences
# import mlbpool.data.teaminfo
# noinspection PyUnresolvedReferences
# import mlbpool.data.passwordreset
# noinspection PyUnresolvedReferences
# import mlbpool.data.picktypes
# noinspection PyUnresolvedReferences
# import mlbpool.data.conferenceinfo
# noinspection PyUnresolvedReferences
# import mlbpool.data.divisioninfo
# noinspection PyUnresolvedReferences
# import mlbpool.data.pick_type_points
# noinspection PyUnresolvedReferences
# import mlbpool.data.picktypes


class DbSessionFactory:
    factory = None

    # Start a database session at app startup
    @staticmethod
    def global_init(db_file):
        if DbSessionFactory.factory:
            return

        if not db_file or not db_file.strip():
            raise Exception("You must specify a data file.")

        conn_str = 'sqlite:///' + db_file
        print("Connecting to db with conn string: {}".format(conn_str))

        engine = sqlalchemy.create_engine(conn_str, echo=False)

        SqlAlchemyBase.metadata.create_all(engine)
        DbSessionFactory.factory = sqlalchemy.orm.sessionmaker(bind=engine)

    @staticmethod
    def create_session():
        return DbSessionFactory.factory()

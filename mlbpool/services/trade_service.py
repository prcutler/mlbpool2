from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.activeplayers import ActiveMLBPlayers
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.teaminfo import TeamInfo


class TradeService:
    """Manage active players who have been traded between the American and National League.  The players need
    to be updated in the database and their stats must be split."""
    @staticmethod
    def pitcher_list():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        pitchers = session.query(ActiveMLBPlayers.player_id, ActiveMLBPlayers.firstname, ActiveMLBPlayers.lastname,
                                    ActiveMLBPlayers.position, TeamInfo.team_abbr)\
            .filter(ActiveMLBPlayers.season == season)\
            .filter(ActiveMLBPlayers.position == 'P')\
            .join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id)\
            .order_by(ActiveMLBPlayers.lastname).all()

        session.close()

        return pitchers

    @staticmethod
    def hitter_list():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        hitters = session.query(ActiveMLBPlayers.player_id, ActiveMLBPlayers.firstname, ActiveMLBPlayers.lastname,
                                    ActiveMLBPlayers.position, TeamInfo.team_abbr)\
            .filter(ActiveMLBPlayers.season == season)\
            .filter(ActiveMLBPlayers.position != 'P')\
            .join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id)\
            .order_by(ActiveMLBPlayers.lastname).all()

        session.close()

        return hitters

    @staticmethod
    def league_list():

        session = DbSessionFactory.create_session()

        leagues = session.query(LeagueInfo).all()

        session.close()

        return leagues

    @staticmethod
    def division_list():

        session = DbSessionFactory.create_session()

        divisions = session.query(DivisionInfo).all()

        session.close()

        return divisions

    @staticmethod
    def team_list():

        session = DbSessionFactory.create_session()

        teams = session.query(TeamInfo).filter(TeamInfo.team_id)\
            .order_by(TeamInfo.name).all()

        session.close()

        return teams

    @staticmethod
    def split_player_stats():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        session.close()

    @classmethod
    def get_pitcher_trade(cls, season: int, player_id: int, team_id: int, games: int, p_wins: int,
                          era: float, er: int, ip: int):
        pass

    @classmethod
    def get_hitter_trade(cls, player_id: int, team_id: int, season: int, hr: int, ba: float, ab: int, hits: int,
                         pa: int, games: int, rbi: int):
        pass

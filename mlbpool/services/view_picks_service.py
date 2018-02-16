from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.account import Account
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.teaminfo import TeamInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.activeplayers import ActiveMLBPlayers
from sqlalchemy import and_


class ViewPicksService:
    @classmethod
    def get_account_info(cls, user_id):
        session = DbSessionFactory.create_session()

        account_info = session.query(Account).filter(Account.id == user_id).all()

        return account_info

    @classmethod
    def seasons_played(cls, user_id):
        session = DbSessionFactory.create_session()

        seasons_played = session.query(PlayerPicks.season).distinct(PlayerPicks.season).filter(Account.id == user_id)

        return seasons_played

    @staticmethod
    def display_picks(user_id, season):

        session = DbSessionFactory.create_session()

        picks_query = session.query(PlayerPicks.pick_type, LeagueInfo.league, DivisionInfo.division,
                                    TeamInfo.name, PlayerPicks.rank,
                                    ActiveMLBPlayers.firstname, ActiveMLBPlayers.lastname, PlayerPicks.multiplier,
                                    PlayerPicks.twins_wins, PlayerPicks.changed) \
            .outerjoin(LeagueInfo)\
            .outerjoin(TeamInfo)\
            .outerjoin(DivisionInfo, and_(PlayerPicks.division_id == DivisionInfo.division_id))\
            .outerjoin(ActiveMLBPlayers, and_(PlayerPicks.player_id == ActiveMLBPlayers.player_id,
                                              PlayerPicks.season == ActiveMLBPlayers.season)).\
            filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season)

        return picks_query

    @staticmethod
    def al_division_winner_picks(user_id, season):
        """Return only the division winner picks in the American League (pick type 1, league_id 0, rank 1)"""

        session = DbSessionFactory.create_session()

        division_winners = session.query(PlayerPicks.pick_type, LeagueInfo.league_id, DivisionInfo.division_id,
                                         TeamInfo.name, PlayerPicks.rank,
                                         PlayerPicks.multiplier, PlayerPicks.changed) \
            .outerjoin(LeagueInfo) \
            .outerjoin(TeamInfo) \
            .outerjoin(DivisionInfo, and_(PlayerPicks.division_id == DivisionInfo.division_id)) \
            .outerjoin(ActiveMLBPlayers, and_(PlayerPicks.player_id == ActiveMLBPlayers.player_id,
                                              PlayerPicks.season == ActiveMLBPlayers.season)). \
            filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season,
                   PlayerPicks.league_id == 0, PlayerPicks.rank == 1, PlayerPicks.pick_type == 1)

        return division_winners

    @staticmethod
    def al_east_picks(user_id, season):
        """Return only the AL East division picks in the American League (pick type 1, league_id 0, division 1)"""

        session = DbSessionFactory.create_session()

        al_east_picks = session.query(PlayerPicks.pick_type, LeagueInfo.league_id, DivisionInfo.division_id,
                                      TeamInfo.name, PlayerPicks.rank,
                                      PlayerPicks.multiplier, PlayerPicks.changed) \
            .outerjoin(LeagueInfo) \
            .outerjoin(TeamInfo) \
            .outerjoin(DivisionInfo, and_(PlayerPicks.division_id == DivisionInfo.division_id)) \
            .outerjoin(ActiveMLBPlayers, and_(PlayerPicks.player_id == ActiveMLBPlayers.player_id,
                                              PlayerPicks.season == ActiveMLBPlayers.season)). \
            filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season,
                   PlayerPicks.league_id == 0, DivisionInfo.division_id == 1, PlayerPicks.pick_type == 1)

        return al_east_picks


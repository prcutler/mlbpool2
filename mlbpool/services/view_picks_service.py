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

        session.close()

        return account_info

    @classmethod
    def seasons_played(cls, user_id):
        session = DbSessionFactory.create_session()

        seasons_played = (
            session.query(PlayerPicks.season)
            .distinct(PlayerPicks.season)
            .filter(Account.id == user_id)
        )

        session.close()

        return seasons_played

    @staticmethod
    def display_picks(user_id, season):

        session = DbSessionFactory.create_session()

        picks_query = (
            session.query(
                PlayerPicks.pick_type,
                LeagueInfo.league,
                DivisionInfo.division,
                TeamInfo.name,
                TeamInfo.team_id,
                PlayerPicks.rank,
                DivisionInfo.division_id,
                LeagueInfo.league_id,
                ActiveMLBPlayers.firstname,
                ActiveMLBPlayers.lastname,
                PlayerPicks.multiplier,
                PlayerPicks.twins_wins,
                PlayerPicks.changed,
                PlayerPicks.player_id,
            )
            .outerjoin(LeagueInfo)
            .outerjoin(TeamInfo)
            .outerjoin(
                DivisionInfo, and_(PlayerPicks.division_id == DivisionInfo.division_id)
            )
            .outerjoin(
                ActiveMLBPlayers,
                and_(
                    PlayerPicks.player_id == ActiveMLBPlayers.player_id,
                    PlayerPicks.season == ActiveMLBPlayers.season,
                ),
            )
            .filter(PlayerPicks.user_id == user_id, PlayerPicks.season == season)
        )

        session.close()

        return picks_query

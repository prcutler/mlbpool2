from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.activeplayers import ActiveMLBPlayers
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.teaminfo import TeamInfo
from mlbpool.data.interleaguetrades import InterleagueTrades
from mlbpool.services.time_service import TimeService


class TradeService:
    """Manage active players who have been traded between the American and National League.  The players need
    to be updated in the database and their stats must be split."""

    @staticmethod
    def pitcher_list():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        pitchers = (
            session.query(
                ActiveMLBPlayers.player_id,
                ActiveMLBPlayers.firstname,
                ActiveMLBPlayers.lastname,
                ActiveMLBPlayers.position,
                TeamInfo.team_abbr,
            )
            .filter(ActiveMLBPlayers.season == season)
            .filter(ActiveMLBPlayers.position == "P")
            .join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id)
            .order_by(ActiveMLBPlayers.lastname)
            .all()
        )

        session.close()

        return pitchers

    @staticmethod
    def hitter_list():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        hitters = (
            session.query(
                ActiveMLBPlayers.player_id,
                ActiveMLBPlayers.firstname,
                ActiveMLBPlayers.lastname,
                ActiveMLBPlayers.position,
                TeamInfo.team_abbr,
            )
            .filter(ActiveMLBPlayers.season == season)
            .filter(ActiveMLBPlayers.position != "P")
            .join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id)
            .order_by(ActiveMLBPlayers.lastname)
            .all()
        )

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

        teams = (
            session.query(TeamInfo)
            .filter(TeamInfo.team_id)
            .order_by(TeamInfo.name)
            .all()
        )

        session.close()

        return teams

    @staticmethod
    def split_player_stats():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        session.close()

    @classmethod
    def get_pitcher_trade(
        cls,
        player_id: int,
        team_id: int,
        games: int,
        saves: int,
        era: float,
        er: int,
        ip: float,
    ):
        # Update the database with the new information

        session = DbSessionFactory.create_session()

        season_row = (
            session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        )
        season = season_row.current_season

        dt = TimeService.get_time()

        for player in (
            session.query(ActiveMLBPlayers.player_id)
            .filter(ActiveMLBPlayers.player_id == player_id)
            .filter(season == season)
        ):
            session.query(ActiveMLBPlayers.player_id).filter(
                ActiveMLBPlayers.team_id
            ).update({"team_id": team_id})

        # Update the InterLeague Trade Table
        pitcher_trade = InterleagueTrades(
            season=season,
            player_id=player_id,
            player_games_played=games,
            saves=saves,
            ERA=era,
            earned_runs=er,
            innings_pitched=ip,
            update_date=dt,
        )
        session.add(pitcher_trade)

        session.commit()
        session.close()

    @classmethod
    def get_hitter_trade(
        cls,
        player_id: int,
        team_id: int,
        hr: int,
        ba: float,
        ab: int,
        hits: int,
        pa: int,
        games: int,
        rbi: int,
    ):

        session = DbSessionFactory.create_session()

        season_row = (
            session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        )
        season = season_row.current_season

        dt = TimeService.get_time()

        # Update the player's team to the new team
        for player in (
            session.query(ActiveMLBPlayers.player_id)
            .filter(ActiveMLBPlayers.player_id == player_id)
            .filter(season == season)
        ):
            session.query(ActiveMLBPlayers.player_id).filter(
                ActiveMLBPlayers.team_id
            ).update({"team_id": team_id})

        # Update the InterLeague Trade Table
        hitter_trade = InterleagueTrades(
            player_id=player_id,
            season=season,
            home_runs=hr,
            batting_average=ba,
            at_bats=ab,
            hits=hits,
            plate_appearances=pa,
            player_games_played=games,
            RBI=rbi,
            update_date=dt,
        )

        session.add(hitter_trade)

        session.commit()
        session.close()

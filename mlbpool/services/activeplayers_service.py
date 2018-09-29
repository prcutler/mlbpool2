import requests
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.activeplayers import ActiveMLBPlayers
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo


class ActivePlayersService:
    """After updating the season to a new year, get all active MLB players and add to the database to be
    used by mlbpool players to choose from when submitting their picks.  The Try / Except is needed for
    players who may not have a position assigned yet."""

    @classmethod
    def add_active_mlbplayers(
        cls,
        season: int,
        team_id: int,
        firstname: str,
        lastname: str,
        position: str,
        player_id: int,
    ):

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            "players.json?season=" + str(season) + "&rosterstatus=assigned-to-roster",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        player_info = response.json()
        player_list = player_info["players"]

        for players in player_list:
            try:
                firstname = players["player"]["firstName"]
                lastname = players["player"]["lastName"]
                player_id = players["player"]["id"]
                team_id = players["player"]["currentTeam"]["id"]
                position = players["player"]["primaryPosition"]
            except TypeError:
                continue

            active_players = ActiveMLBPlayers(
                firstname=firstname,
                lastname=lastname,
                player_id=player_id,
                team_id=team_id,
                position=position,
                season=season,
            )

            session.add(active_players)

            session.commit()
            session.close()

    @staticmethod
    def update_mlbplayers():

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            "players.json?season=" + str(season) + "&rosterstatus=assigned-to-roster",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        player_info = response.json()
        player_list = player_info["players"]

        player_tuple = (
            session.query(ActiveMLBPlayers.player_id)
            .filter(ActiveMLBPlayers.season == season)
            .all()
        )
        current_players = [sql_players for sql_players, in player_tuple]
        print(current_players)

        for players in player_list:

            try:

                firstname = players["player"]["firstName"]
                lastname = players["player"]["lastName"]
                player_id = players["player"]["id"]
                team_id = players["player"]["currentTeam"]["id"]
                position = players["player"]["primaryPosition"]

            except KeyError:
                continue

            if int(player_id) not in current_players:

                updated_players = ActiveMLBPlayers(
                    firstname=firstname,
                    lastname=lastname,
                    player_id=player_id,
                    team_id=team_id,
                    position=position,
                    season=season,
                )

                session.add(updated_players)

                session.commit()

            else:
                pass

            session.close()

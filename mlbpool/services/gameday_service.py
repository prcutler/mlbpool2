import pendulum
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory


class GameDayService:

    @staticmethod
    def get_season_opener_info:
        """Get the date of the season opener"""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()

        season = season_row.current_season
        season_opener_date = session.query(SeasonInfo.season_start_date)
        all_star_game_date = session.query(SeasonInfo.all_star_game_date)
        tz = pendulum.timezone('America/New_York')

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats==HR,AVG,RBI',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        gameday_json = response.json()
        gameday_data = gameday_json["cumulativeplayerstats"]["playerstatsentry"]

        for gameday_info in gameday_data:
            first_game = fullgameschedule["gameentry"][0]
            first_game_date = first_game["date"]
            first_game_time = first_game["time"]
            away_team = first_game["awayTeam"]["Name"]
            home_team = first_game["homeTeam"]["Name"]


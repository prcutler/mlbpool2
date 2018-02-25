from mlbpool.data.dbsession import DbSessionFactory
import requests
from mlbpool.data.weekly_mlbplayer_stats import WeeklyMLBPlayerStats
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.weekly_team_stats import WeeklyTeamStats
import datetime


def get_seasons():
    """Get the current active season from the database"""
    session = DbSessionFactory.create_session()
    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
    current_season = season_row.current_season

    session.close()

    return current_season


def get_update_date():
    """Get the date of the update to insert into the database"""

    # TODO Move to Pendulum and determine how I want the update to show up since MLB does not have to be weekly

    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    stats_date = today - one_day

    return stats_date


class WeeklyStatsService:
    """Open a connection to the database to get the current season year from the SeasonInfo table
    Get weekly stats for each player for hitting (batting average, home runs and RBIs) and pitching (ERA and
    wins by pitcher)"""
    @staticmethod
    def get_hitter_stats():
        """Get stats for hitters (home runs, batting average and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats==HR,AVG,RBI',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        player_json = response.json()
        player_data = player_json["cumulativeplayerstats"]["playerstatsentry"]

        for players in player_data:
            try:
                player_id = players["player"]["ID"]
                home_runs = players["stats"]["Homeruns"]["#text"]
                RBI = players["stats"]["RunsBattedIn"]["#text"]
                batting_average = players["stats"]["BattingAvg"]["#text"]
                plate_appearances = players["stats"]["PlateAppearances"]["#text"]
                player_games_played = players["stats"]["GamesPlayed"]["#text"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(player_id=player_id, season=season, home_runs=home_runs,
                                                       RBI=RBI, batting_average=batting_average,
                                                       plate_appearance=plate_appearances,
                                                       player_games_played=player_games_played,
                                                       update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

    @staticmethod
    def get_pitcher_stats():
        """Get cumulative Pitcher stats (wins and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats==W,ERA',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        player_json = response.json()
        player_data = player_json["cumulativeplayerstats"]["playerstatsentry"]

        for players in player_data:
            try:
                player_id = players["player"]["ID"]
                ERA = players["stats"]["EarnedRunAvg"]["#text"]
                pitcher_wins = players["stats"]["Wins"]["#text"]
                innings_pitched = players["stats"]["InningsPitched"]["#text"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(player_id=player_id, season=season,
                                                       ERA=ERA, pitcher_wins=pitcher_wins,
                                                       update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

    # Get the weekly rank for each team in each division sorted by division
    @staticmethod
    def get_team_rankings():
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/division_team_standings.json?teamstats=W',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        team_json = response.json()
        team_data = team_json["divisionteamstandings"]["division"]

        x = 0
        y = 0
        z = 0

        while x < len(team_data):
            rank = (team_data[x]["teamentry"][1]["rank"])
            team_id = (team_data[x]["teamentry"][1]["team"]["ID"])

            x += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while y < len(team_data):
            rank = (team_data[y]["teamentry"][0]["rank"])
            team_id = (team_data[y]["teamentry"][0]["team"]["ID"])

            y += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while z < len(team_data):
            rank = (team_data[z]["teamentry"][2]["rank"])
            team_id = (team_data[z]["teamentry"][2]["team"]["ID"])

            z += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

    @staticmethod
    def get_league_standings():
        """Get the rank of each team in each league (1-15) and also how many games each team has played"""
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/conference_team_standings.json?teamstats=W',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        x = 0
        y = 0

        data = response.json()
        teamlist = data["conferenceteamstandings"]["conference"][0]["teamentry"]

        for al_teams in teamlist:
            team_id = int(data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["ID"])
            league_rank = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["rank"]
            games_played =  data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["stats"]["GamesPlayed"]

            x += 1

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"league_rank": league_rank}, {"team_games_played": games_played})

            session.commit()

        for nl_team_list in teamlist:
            team_id = int(data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["ID"])
            league_rank = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["rank"]
            games_played = data["conferenceteamstandings"]["conference"][1]["teamentry"][x]["stats"]["GamesPlayed"]

            y += 1

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"league_rank": league_rank}, {"games_played": games_played})

            session.commit()

    @staticmethod
    def get_tiebreaker():
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        update_date = get_update_date()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/overall_team_standings.json?teamstats=W',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        team_json = response.json()
        team_data = team_json["overallteamstandings"]["teamstandingsentry"]

        for teams in team_data:
            team_id = teams["team"]["ID"]["120"]
            twins_wins = teams["stats"]["Wins"]["#text"]

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id)\
                .filter(update_date == update_date) \
                .update({"tiebreaker_twin_wins": twins_wins})

            session.commit()




from mlbpool.data.dbsession import DbSessionFactory
import requests
from mlbpool.data.weekly_mlbplayer_stats import WeeklyMLBPlayerStats
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.weekly_team_stats import WeeklyTeamStats
import pendulum
from mlbpool.data.weekly_al_player_stats import WeeklyALPlayerStats
from mlbpool.data.weekly_nl_player_stats import WeeklyNLPlayerStats



def get_seasons():
    """Get the current active season from the database"""
    session = DbSessionFactory.create_session()
    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
    current_season = season_row.current_season

    session.close()

    return current_season


def get_update_date():
    """Get the date of the update to insert into the database"""

    today = pendulum.now()
    stats_date = today.subtract(days=1)

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
                                '-regular/cumulative_player_stats.json?playerstats=HR,AVG,RBI,PA,H,AB'
                                '&position=C,1B,2B,SS,3B,OF,RF,CF,LF,DH',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        player_json = response.json()
        player_data = player_json["cumulativeplayerstats"]["playerstatsentry"]

        for players in player_data:
            try:
                player_id = players["player"]["ID"]
                home_runs = players["stats"]["Homeruns"]["#text"]
                RBI = players["stats"]["RunsBattedIn"]["#text"]
                batting_average = players["stats"]["BattingAvg"]["#text"]
                at_bats = players["stats"]["AtBats"]["#text"]
                hits = players["stats"]["Hits"]["#text"]
                plate_appearances = players["stats"]["PlateAppearances"]["#text"]
                player_games_played = players["stats"]["GamesPlayed"]["#text"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(player_id=player_id, season=season, home_runs=home_runs,
                                                       RBI=RBI, batting_average=batting_average,
                                                       at_bats=at_bats, hits=hits,
                                                       plate_appearances=plate_appearances,
                                                       player_games_played=player_games_played,
                                                       update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_al_hitter_stats():
        """Get stats for hitters (home runs, batting average and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats=HR,AVG,RBI,PA'
                                '&position=C,1B,2B,SS,3B,OF&team=BAL,BOS,NYY,TB,CLE,DET,KC,CWS,MIN,TEX,HOU,SEA,LAA,OAK',
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

            weekly_player_stats = WeeklyALPlayerStats(player_id=player_id, season=season, home_runs=home_runs,
                                                      RBI=RBI, batting_average=batting_average,
                                                      plate_appearances=plate_appearances,
                                                      player_games_played=player_games_played,
                                                      update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_pitcher_stats():
        """Get cumulative Pitcher stats (wins and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats=W,ERA,IP,ER&position=P',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        player_json = response.json()
        player_data = player_json["cumulativeplayerstats"]["playerstatsentry"]

        for players in player_data:
            try:
                player_id = players["player"]["ID"]
                ERA = players["stats"]["EarnedRunAvg"]["#text"]
                pitcher_wins = players["stats"]["Wins"]["#text"]
                earned_runs = players["stats"]["EarnedRunsAllowed"]["#text"]
                innings_pitched = players["stats"]["InningsPitched"]["#text"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(player_id=player_id, season=season,
                                                       ERA=ERA, pitcher_wins=pitcher_wins,
                                                       earned_runs=earned_runs,
                                                       innings_pitched=innings_pitched,
                                                       update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_al_pitcher_stats():
        """Get cumulative Pitcher stats (wins and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats=W,ERA,IP&position=P'
                                '&team=&team=BAL,BOS,NYY,TB,CLE,DET,KC,CWS,MIN,TEX,HOU,SEA,LAA,OAK',
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

            weekly_player_stats = WeeklyALPlayerStats(player_id=player_id, season=season,
                                                      ERA=ERA, pitcher_wins=pitcher_wins,
                                                      innings_pitched=innings_pitched,
                                                      update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_nl_hitter_stats():
        """Get stats for hitters (home runs, batting average and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats=HR,AVG,RBI,PA'
                                '&position=C,1B,2B,SS,3B,OF'
                                '&team=WAS,NYM,MIA,PHI,ATL,CHC,PIT,STL,MIL,CIN,SF,LAD,COL,SD,ARI',
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

            weekly_player_stats = WeeklyNLPlayerStats(player_id=player_id, season=season, home_runs=home_runs,
                                                      RBI=RBI, batting_average=batting_average,
                                                      plate_appearances=plate_appearances,
                                                      player_games_played=player_games_played,
                                                      update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_nl_pitcher_stats():
        """Get cumulative Pitcher stats (wins and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        season_start = session.query(SeasonInfo).filter(SeasonInfo.season_start_date == '1').first()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/cumulative_player_stats.json?playerstats=W,ERA,IP&position=P'
                                '&team=&team=WAS,NYM,MIA,PHI,ATL,CHC,PIT,STL,MIL,CIN,SF,LAD,COL,SD,ARI',
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

            weekly_player_stats = WeeklyNLPlayerStats(player_id=player_id, season=season,
                                                      ERA=ERA, pitcher_wins=pitcher_wins,
                                                      innings_pitched=innings_pitched,
                                                      update_date=update_date)

            session.add(weekly_player_stats)

            session.commit()

            session.close()

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
        a = 0
        b = 0

        while x < len(team_data):
            rank = (team_data[x]["teamentry"][1]["rank"])
            team_id = (team_data[x]["teamentry"][1]["team"]["ID"])
            team_wins = team_data[x]["teamentry"][1]["stats"]["Wins"]["#text"]

            x += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season, team_wins=team_wins,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while y < len(team_data):
            rank = (team_data[y]["teamentry"][0]["rank"])
            team_id = (team_data[y]["teamentry"][0]["team"]["ID"])
            team_wins = team_data[y]["teamentry"][1]["stats"]["Wins"]["#text"]

            y += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season, team_wins=team_wins,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while z < len(team_data):
            rank = (team_data[z]["teamentry"][2]["rank"])
            team_id = (team_data[z]["teamentry"][2]["team"]["ID"])
            team_wins = team_data[z]["teamentry"][1]["stats"]["Wins"]["#text"]

            z += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season, team_wins=team_wins,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while a < len(team_data):
            rank = (team_data[a]["teamentry"][3]["rank"])
            team_id = (team_data[a]["teamentry"][3]["team"]["ID"])
            team_wins = team_data[a]["teamentry"][1]["stats"]["Wins"]["#text"]

            a += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season, team_wins=team_wins,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

        while b < len(team_data):
            rank = (team_data[b]["teamentry"][4]["rank"])
            team_id = (team_data[b]["teamentry"][4]["team"]["ID"])
            team_wins = team_data[b]["teamentry"][1]["stats"]["Wins"]["#text"]

            b += 1

            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(team_id=team_id, season=season, team_wins=team_wins,
                                                division_rank=rank, update_date=update_date)

            session.add(weekly_team_stats)
            session.commit()

            session.close()

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
            games_played = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["stats"]["GamesPlayed"]["#text"]

            x += 1

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"team_games_played": games_played})

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"league_rank": league_rank})

            session.commit()

        for nl_team_list in teamlist:
            team_id = int(data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["ID"])
            league_rank = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["rank"]
            games_played = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["stats"]["GamesPlayed"]["#text"]

            y += 1

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"team_games_played": games_played})

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == team_id). \
                update({"league_rank": league_rank})

            session.commit()

        session.close()

    @staticmethod
    def get_tiebreaker():
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        update_date = get_update_date()

        response = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/' + str(season) +
                                '-regular/overall_team_standings.json?teamstats=W&team=120',
                                auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

        team_json = response.json()
        team_data = team_json["overallteamstandings"]["teamstandingsentry"]

        for teams in team_data:
            twins_wins = teams["stats"]["Wins"]["#text"]

            session.query(WeeklyTeamStats).filter(WeeklyTeamStats.team_id == 120)\
                .filter(update_date == update_date) \
                .update({"tiebreaker_twin_wins": twins_wins})

            session.commit()

            session.close()


    @staticmethod
    def trade_adjustments():
        season = get_seasons()

        session = DbSessionFactory.create_session()
        #ASSUMES players are either pitcher or not
        # update all except batting average
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET w.home_runs = (w.home_runs - i.home_runs), "
        sqlstr += "w.at_bats = (w.at_bats - i.at_bats), "
        sqlstr += "w.hits = (w.hits - i.hits), "
        sqlstr += "w.plate_appearances = (w.RBI - i.RBI) "
        sqlstr += "WHERE w.batting_average IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)
        session.execute(sqlstr)
        session.commit()
        #print(sqlstr)

        # update batting average
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET w.batting_average = (w.hits / w.at_bats) "
        sqlstr += "WHERE w.batting_average IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)
        session.execute(sqlstr)
        session.commit()
        #print(sqlstr)

        #pitchers
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET w.pitcher_wins = (w.pitcher_wins-i.pitcher_wins), "
        sqlstr += "w.earned_runs = (w.earned_runs-i.earned_runs), "
        sqlstr += "w.innings_pitched=(w.innings_pitched-i.innings_pitched) "
        sqlstr += "WHERE w.ERA IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)
        session.execute(sqlstr)
        session.commit()
        #print(sqlstr)

        #pitchers update ERA
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET "
        sqlstr += "w.ERA = ROUND(((w.earned_runs/w.innings_pitched)*9),2) "
        sqlstr += "WHERE w.ERA IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)

        #print(sqlstr)

        session.execute(sqlstr)
        session.commit()

        session.close()
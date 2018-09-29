from mlbpool.data.dbsession import DbSessionFactory
import requests
from mlbpool.data.weekly_mlbplayer_stats import WeeklyMLBPlayerStats
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.weekly_team_stats import WeeklyTeamStats
from mlbpool.services.time_service import TimeService


def get_seasons():
    """Get the current active season from the database"""
    session = DbSessionFactory.create_session()
    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
    current_season = season_row.current_season

    session.close()

    return current_season


def get_update_date():
    """Get the date of the update to insert into the database"""

    today = TimeService.get_time()
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

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            + str(season)
            + "-regular/player_stats_totals.json?position=C,1B,2B,SS,3B,OF,RF,CF,LF,DH",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        player_json = response.json()
        player_data = player_json["playerStatsTotals"]

        for players in player_data:
            try:
                player_id = players["player"]["id"]
                home_runs = players["stats"]["batting"]["homeruns"]
                RBI = players["stats"]["batting"]["runsBattedIn"]
                batting_average = players["stats"]["batting"]["battingAvg"]
                at_bats = players["stats"]["batting"]["atBats"]
                hits = players["stats"]["batting"]["hits"]
                plate_appearances = players["stats"]["batting"]["plateAppearances"]
                player_games_played = players["stats"]["gamesPlayed"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(
                player_id=player_id,
                season=season,
                home_runs=home_runs,
                RBI=RBI,
                batting_average=batting_average,
                at_bats=at_bats,
                hits=hits,
                plate_appearances=plate_appearances,
                player_games_played=player_games_played,
                update_date=update_date,
            )

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    @staticmethod
    def get_pitcher_stats():
        """Get cumulative Pitcher stats (wins and ERA) from MySportsFeeds and insert into the database"""

        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            + str(season)
            + "-regular/player_stats_totals.json?position=P",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        player_json = response.json()
        player_data = player_json["playerStatsTotals"]

        for players in player_data:
            try:
                player_id = players["player"]["id"]
                ERA = players["stats"]["pitching"]["earnedRunAvg"]
                pitcher_wins = players["stats"]["pitching"]["wins"]
                earned_runs = players["stats"]["pitching"]["earnedRunsAllowed"]
                innings_pitched = players["stats"]["pitching"]["inningsPitched"]

            except KeyError:
                continue

            update_date = get_update_date()

            weekly_player_stats = WeeklyMLBPlayerStats(
                player_id=player_id,
                season=season,
                ERA=ERA,
                pitcher_wins=pitcher_wins,
                earned_runs=earned_runs,
                innings_pitched=innings_pitched,
                update_date=update_date,
            )

            session.add(weekly_player_stats)

            session.commit()

            session.close()

    # Get the weekly rank for each team in each division sorted by division
    @staticmethod
    def get_team_rankings():
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            + str(season)
            + "-regular/standings.json",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        standings_json = response.json()
        standings_data = standings_json["teams"]

        x = 0

        for teams in standings_data:
            team_id = standings_data[x]["team"]["id"]
            division_rank = standings_data[x]["divisionRank"]["rank"]
            playoff_rank = standings_data[x]["playoffRank"]["rank"]
            team_wins = standings_data[x]["stats"]["standings"]["wins"]
            games_played = standings_data[x]["stats"]["gamesPlayed"]
            update_date = get_update_date()

            weekly_team_stats = WeeklyTeamStats(
                team_id=team_id,
                season=season,
                team_wins=team_wins,
                division_rank=division_rank,
                league_rank=playoff_rank,
                team_games_played=games_played,
                update_date=update_date,
            )

            x += 1

            session.add(weekly_team_stats)
            session.commit()

        session.close()

    @staticmethod
    def get_tiebreaker():
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
        season = season_row.current_season

        update_date = get_update_date()

        response = requests.get(
            "https://api.mysportsfeeds.com/v2.0/pull/mlb/"
            + str(season)
            + "-regular/standings.json?team=120",
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw),
        )

        team_json = response.json()
        team_data = team_json["teams"]

        for teams in team_data:
            twins_wins = teams["stats"]["standings"]["wins"]

            session.query(WeeklyTeamStats).filter(
                WeeklyTeamStats.team_id == 120
            ).filter(update_date == update_date).filter(season == season).update(
                {"tiebreaker_twin_wins": twins_wins}
            )

            session.commit()

            session.close()

    @staticmethod
    def trade_adjustments():
        season = get_seasons()

        session = DbSessionFactory.create_session()
        # ASSUMES players are either pitcher or not
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
        # print(sqlstr)

        # update batting average
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET w.batting_average = (w.hits / w.at_bats) "
        sqlstr += "WHERE w.batting_average IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)
        session.execute(sqlstr)
        session.commit()
        # print(sqlstr)

        # pitchers
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
        # print(sqlstr)

        # pitchers update ERA
        sqlstr = "UPDATE WeeklyMLBPlayerStats w "
        sqlstr += "INNER JOIN InterleagueTrades i "
        sqlstr += "ON i.player_id = w.player_id AND i.season=w.season "
        sqlstr += "SET "
        sqlstr += "w.ERA = ROUND(((w.earned_runs/w.innings_pitched)*9),2) "
        sqlstr += "WHERE w.ERA IS NOT NULL "
        sqlstr += "AND w.season=" + str(season)

        # print(sqlstr)

        session.execute(sqlstr)
        session.commit()

        session.close()

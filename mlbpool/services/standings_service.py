from mlbpool.data.dbsession import DbSessionFactory
from sqlalchemy.orm import joinedload
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.weekly_player_results import WeeklyPlayerResults
from _datetime import datetime
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.account import Account


def get_seasons():
    session = DbSessionFactory.create_session()
    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
    current_season = season_row.current_season

    session.close()

    return current_season


def get_week():
    # TODO This needs to be re-written - not using weeks in MLBPool
    session = DbSessionFactory.create_session()

    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
    season_start = season_row.season_start_date
    season_start = datetime.strptime(season_start, "%Y-%m-%d")

    diff = datetime.now() - season_start
    print(diff.days)
    week = int((diff.days / 7) + 1)
    print(week)

#    week = 17           # ------------------------------- TESTING ------------------- remove this line after test.

    session.close()

    return week


class StandingsService:
    def display_player_standings(player_id, season=None):
        if season is None:
            season = get_seasons()

        sqlstr = "SELECT coalesce(w.points_earned,0) as points, a.first_name, a.last_name, w.pick_id, p.pick_type, p.rank, p.multiplier, t.name, "
        sqlstr += "c.league, d.division, ap.firstname, ap.lastname "
        sqlstr += "FROM PlayerPicks p, Account a "
        sqlstr += "LEFT JOIN WeeklyPlayerResults w on p.pick_id = w.pick_id "
        sqlstr += "AND w.week = (SELECT MAX(week) from WeeklyPlayerResults  WHERE season=" + str(season) + ") "
        sqlstr += "LEFT JOIN  DivisionInfo d on p.division_id=d.division_id "
        sqlstr += "LEFT JOIN LeagueInfo c ON p.league_id= c.league_id "
        sqlstr += "LEFT JOIN TeamInfo t ON p.team_id = t.team_id "
        sqlstr += "LEFT JOIN ActiveMLBPlayers ap ON p.player_id = ap.player_id AND p.season = ap.season "
        sqlstr += "WHERE "
        sqlstr += "p.user_id = a.id "
        sqlstr += "AND p.season = " + str(season) + " "
        sqlstr += "AND p.user_id = '" + player_id +"'"

        session = DbSessionFactory.create_session()
        standings = session.execute(sqlstr)

        dict_standings = [dict(row) for row in standings]

        session.close()

        return dict_standings

    def display_weekly_standings(season=None):

        # return list that contains player standings for most recent week in results table
        if season is None:
            season = get_seasons()

        sqlstr = "SELECT SUM(w.points_earned) as total_points, a.first_name, a.last_name, a.id from WeeklyPlayerResults w, PlayerPicks p, Account a "
        sqlstr += "WHERE w.pick_id = p.pick_id AND p.user_id = a.id "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += "AND w.week = (SELECT MAX(week) from WeeklyPlayerResults WHERE season = " + str(season) + ") "
        sqlstr += "GROUP BY p.user_id "
        sqlstr += "ORDER BY total_points DESC"

        session = DbSessionFactory.create_session()
        standings = session.execute(sqlstr)

        dict_standings = [dict(row) for row in standings]

        session.close()

        return dict_standings

    @staticmethod
    def update_player_pick_points():

        # TODO Kelly - Is this where we add / calculate the ERA and BA qualifiers?
        """ Batting Average qualifier - A player must have 3.1 plate appearances (PA) per team game (
        for a total of 502 over the current 162-game season) to qualify for the batting title.
        Plate Appearances is a column in WeeklyMLBPlayers.  team_games_played is in WeeklyTeamStats.

        A pitcher to pitch one inning per game played by their team. In most years, that is 162 innings.
        team_games_played is in WeeklyTeamStats."""

        season = get_seasons()
        week = get_week()

        session = DbSessionFactory.create_session()

        # starting values
        league = 0
        i = 4

        while league < 2:
            # start with pick type 4 and continue through 8

            if i == 4:
                cattype = "homeruns"
            elif i == 5:
                cattype ="batting_average"
            elif i == 6:
                cattype ="RBI"
            elif i == 7:
                cattype ="pitcher_wins"
            elif i == 8:
                cattype = "ERA"


            sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, week, points_earned) "
            sqlstr += "SELECT t1.pick_id as pick_id, t1.season as season, t1.week as week, pts.points*t1.multiplier as points_earned "
            sqlstr += "FROM "
            sqlstr += "(SELECT p.pick_id, p.user_id, p.multiplier, p.player_id, "
            sqlstr += "(SELECT count(*) from WeeklyMLBPlayerStats as w2, ActiveMLBPlayers as ap, "
            sqlstr += "TeamInfo as t "
            sqlstr += "WHERE "
            sqlstr += "w2.week = " + str(week) + " "
            sqlstr += "AND w2.season = " + str(season) + " "
            sqlstr += "AND w2.player_id = ap.player_id "
            sqlstr += "AND ap.team_id = t.team_id "
            sqlstr += "AND t.league_id = " + str(league) + " "
            sqlstr += "AND W2." + cattype + ">w." + cattype + ")+1 as rank, "
            sqlstr += "w.week, "
            sqlstr += "w.season "
            sqlstr += "FROM WeeklyMLBPlayerStats w, PlayerPicks p "
            sqlstr += "WHERE w.player_id = p.player_id "
            sqlstr += "AND  w.season = " + str(season) + " "
            sqlstr += "AND w.week = " + str(week) + " "
            sqlstr += "AND p.pick_type = " + str(i) + " "
            sqlstr += "AND p.league_id = " + str(league) + " "
            sqlstr += "AND w." + cattype + " not null "
            sqlstr += "ORDER BY rank) as t1, PickTypePoints pts "
            sqlstr += "WHERE "
            sqlstr += "pts.pick_type_id = " + str(i) + " "
            sqlstr += "AND t1.rank = pts.place"

            session.execute(sqlstr)
            session.commit()

            # increment counters
            if i == 8:
                league += 1
                i = 0

            i += 1

        session.close()

    @staticmethod
    def update_team_pick_points():
        session = DbSessionFactory.create_session()

        season = get_seasons()
        week = get_week()

        # this does all type 1 points
        sqlstr = "INSERT INTO WeeklyPlayerResults(pick_id, season, week, points_earned) "
        sqlstr += "SELECT pp.pick_id, w.season, w.week, p.points * pp.multiplier as points_earned "
        sqlstr += "FROM PlayerPicks pp "
        sqlstr += "LEFT JOIN WeeklyTeamStats w on pp.rank=w.division_rank and pp.team_id=w.team_id "
        sqlstr += "LEFT JOIN TeamInfo t on pp.team_id= t.team_id "
        sqlstr += "LEFT JOIN PickTypePoints p on pp.pick_type = p.pick_type_id "
        sqlstr += "WHERE pp.pick_type = 1 "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += "AND w.week = " + str(week) + " "
        sqlstr += "AND pp.league_id = t.league_id "
        sqlstr += "AND pp.division_id = t.division_id "
        sqlstr += "AND p.place = w.division_rank "
        sqlstr += "ORDER BY pp.user_id"

        session.execute(sqlstr)
        session.commit()

        # type 3 team wins points:
        # TODO Need a similar function for type 2 - team losses - Kelly
        league = 0
        while league < 2:
            sqlstr = "INSERT INTO WeeklyPlayerResults(pick_id, season, week, points_earned) "
            sqlstr += "SELECT t1.pick_id as pick_id, t1.season as season, t1.week as week, pts.points * t1.multiplier as points_earned "
            sqlstr += "FROM (SELECT p.pick_id, p.user_id, p.multiplier, p.team_id, "
            sqlstr += "(SELECT count(*) FROM WeeklyTeamStats as w2, TeamInfo as t "
            sqlstr += "WHERE w2.team_id = t.team_id "
            sqlstr += "AND w2.week = " + str(week) + " "
            sqlstr += "AND w2.season = " + str(season) + " "
            sqlstr += "AND t.league_id = " + str(league) + " "
            sqlstr += "AND w2.points_for > w.points_for)+1 as rank, "
            sqlstr += "w.week, w.season "
            sqlstr += "FROM WeeklyTeamStats w, PlayerPicks p "
            sqlstr += "WHERE w.team_id = p.team_id "
            sqlstr += "AND w.season = " + str(season) + " "
            sqlstr += "AND w.week = " + str(week) + " "
            sqlstr += "AND p.pick_type = 3 "
            sqlstr += "AND p.league_id = " + str(league) + " "
            sqlstr += "AND w.points_for not null "
            sqlstr += "ORDER BY rank) as t1, PickTypePoints pts "
            sqlstr += "WHERE "
            sqlstr += "pts.pick_type_id = 3 "
            sqlstr += "AND t1.rank = pts.place"

            session.execute(sqlstr)
            session.commit()
            league += 1

        # type 9 points - wildcard - (rank 4,5 - NFLPool was 5,6)
        sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, week, points_earned) "
        sqlstr += "SELECT p.pick_id, w.season, w.week, pts.points*p.multiplier as points_earned from PlayerPicks p, WeeklyTeamStats w, PickTypePoints pts "
        sqlstr += "WHERE p.pick_type = 9 "
        sqlstr += "AND p.pick_type = pts.pick_type_id "
        sqlstr += "AND w.league_rank in (4,5) "
        sqlstr += "AND w.team_id = p.team_id "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += "AND w.week = " + str(week)

        session.execute(sqlstr)
        session.commit()

        session.close()

    @staticmethod
    def all_seasons_played():
        """This method is used to get a list of all seasons played and display on the Standings index page
        for players to click through to see the season standings / points scored by player"""
        session = DbSessionFactory.create_session()

        seasons_played = session.query(PlayerPicks.season).distinct(PlayerPicks.season)

        session.close()

        return seasons_played



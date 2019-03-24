from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks
from sqlalchemy import func
from mlbpool.data.weekly_mlbplayer_stats import WeeklyMLBPlayerStats
from mlbpool.data.seasoninfo import SeasonInfo


def get_seasons():
    session = DbSessionFactory.create_session()
    season_row = session.query(SeasonInfo).filter(SeasonInfo.id == "1").first()
    current_season = season_row.current_season

    session.close()

    return current_season


def get_update_players_date(season):
    session = DbSessionFactory.create_session()
    qry = session.query(func.max(WeeklyMLBPlayerStats.update_date).label("max"))
    res = qry.one()
    latest_date = res.max
    session.close()
    return latest_date


class StandingsService:
    def display_player_standings(player_id, season=None):
        if season is None:
            season = get_seasons()

        sqlstr = "SELECT DISTINCT(w.pick_id), coalesce(w.points_earned,0) as points, a.first_name, a.last_name, p.pick_type, p.rank, p.multiplier, t.name, p.changed, "
        sqlstr += "c.league, d.division, ap.firstname, ap.lastname "
        sqlstr += "FROM (PlayerPicks p, Account a) "
        sqlstr += "LEFT JOIN WeeklyPlayerResults w on p.pick_id = w.pick_id "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyPlayerResults WHERE season="
            + str(season)
            + ") "
        )
        sqlstr += "LEFT JOIN  DivisionInfo d on p.division_id=d.division_id "
        sqlstr += "LEFT JOIN LeagueInfo c ON p.league_id= c.league_id "
        sqlstr += "LEFT JOIN TeamInfo t ON p.team_id = t.team_id "
        sqlstr += "LEFT JOIN ActiveMLBPlayers ap ON p.player_id = ap.player_id AND p.season = ap.season "
        sqlstr += "WHERE "
        sqlstr += "p.user_id = a.id "
        sqlstr += "AND p.season = " + str(season) + " "
        sqlstr += "AND p.user_id = '" + player_id + "'"

        # print(sqlstr)

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
        sqlstr += "AND p.season=w.season "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyPlayerResults WHERE season = "
            + str(season)
            + ") "
        )
        sqlstr += "GROUP BY p.user_id "
        sqlstr += "ORDER BY total_points DESC"

        #print(sqlstr)

        session = DbSessionFactory.create_session()
        standings = session.execute(sqlstr)

        dict_standings = [dict(row) for row in standings]

        session.close()

        return dict_standings

    @staticmethod
    def update_player_pick_points():
        """ Batting Average qualifier - A player must have 3.1 plate appearances (PA) per team game (
        for a total of 502 over the current 162-game season) to qualify for the batting title.
        Plate Appearances is a column in WeeklyMLBPlayers.  team_games_played is in WeeklyTeamStats.
        A pitcher to pitch one inning per game played by their team. In most years, that is 162 innings.
        team_games_played is in WeeklyTeamStats."""

        season = get_seasons()

        last_update = get_update_players_date(season)

        session = DbSessionFactory.create_session()

        # starting values
        league = 0
        i = 4

        while league < 2:
            # start with pick type 4 and continue through 8

            if i == 4:
                cattype = "home_runs"
            elif i == 5:
                cattype = "batting_average"
            elif i == 6:
                cattype = "RBI"
            elif i == 11:
                cattype = "saves"
            elif i == 8:
                cattype = "ERA"

            if i == 4 or i == 6 or i == 11:
                sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, update_date, points_earned) "
                sqlstr += "SELECT t1.pick_id as pick_id, t1.season as season, t1.update_date as update_date, (pts.points*t1.multiplier*t1.changed) as points_earned "
                sqlstr += "FROM "
                sqlstr += "(SELECT DISTINCT p.pick_id, p.user_id, p.multiplier, IF(p.changed=1,0.5,1) as changed, p.player_id, "
                sqlstr += "(SELECT count(*) from WeeklyMLBPlayerStats as w2, ActiveMLBPlayers as ap, "
                sqlstr += "TeamInfo as t "
                sqlstr += "WHERE "
                sqlstr += "w2.update_date = '" + str(last_update) + "' "
                sqlstr += "AND w2.season = " + str(season) + " "
                sqlstr += "AND ap.season = w2.season "
                sqlstr += "AND w2.player_id = ap.player_id "
                sqlstr += "AND ap.team_id = t.team_id "
                sqlstr += "AND t.league_id = " + str(league) + " "
                sqlstr += "AND w2." + cattype + ">w." + cattype + ")+1 as rank, "
                sqlstr += "w.update_date, "
                sqlstr += "w.season "
                sqlstr += "FROM WeeklyMLBPlayerStats w, PlayerPicks p "
                sqlstr += "WHERE w.player_id = p.player_id "
                sqlstr += "AND  w.season = " + str(season) + " "
                sqlstr += "AND w.update_date = '" + str(last_update) + "' "
                sqlstr += "AND p.pick_type = " + str(i) + " "
                sqlstr += "AND p.league_id = " + str(league) + " "
                sqlstr += "AND w." + cattype + " IS NOT NULL "
                sqlstr += "ORDER BY rank) as t1, PickTypePoints pts "
                sqlstr += "WHERE "
                sqlstr += "pts.pick_type_id = " + str(i) + " "
                sqlstr += "AND t1.rank = pts.rank"
                session.execute(sqlstr)
                session.commit()

            elif i == 5:
                sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, update_date, points_earned) "
                sqlstr += "SELECT t1.pick_id as pick_id, t1.season as season, t1.update_date as update_date, (pts.points*t1.multiplier*t1.changed) as points_earned "
                sqlstr += "FROM "
                sqlstr += "(SELECT DISTINCT p.pick_id, p.user_id, p.multiplier, IF(p.changed=1,0.5,1) as changed, p.player_id, "
                sqlstr += "(SELECT count(*) from WeeklyMLBPlayerStats as w2, ActiveMLBPlayers as ap, "
                sqlstr += "TeamInfo as t, WeeklyTeamStats as wt  "
                sqlstr += "WHERE "
                sqlstr += "w2.update_date = '" + str(last_update) + "' "
                sqlstr += "AND w." + cattype + " IS NOT NULL "
                sqlstr += "AND w2.season = " + str(season) + " "
                sqlstr += "AND ap.season = w2.season "
                sqlstr += "AND w2.player_id = ap.player_id "
                sqlstr += "AND ap.team_id = t.team_id "
                sqlstr += "AND ap.team_id = wt.team_id "
                sqlstr += "AND wt.update_date = '" + str(last_update) + "' "
                sqlstr += "AND t.league_id = " + str(league) + " "
                sqlstr += "AND w2.plate_appearances >= (3.1*wt.team_games_played) "
                sqlstr += "AND w2." + cattype + ">w." + cattype + ")+1 as rank, "
                sqlstr += "w.update_date, "
                sqlstr += "w.season "
                sqlstr += "FROM WeeklyMLBPlayerStats w, PlayerPicks p "
                sqlstr += "WHERE w.player_id = p.player_id "
                sqlstr += "AND  w.season = " + str(season) + " "
                sqlstr += "AND w.update_date = '" + str(last_update) + "' "
                sqlstr += "AND p.pick_type = " + str(i) + " "
                sqlstr += "AND p.league_id = " + str(league) + " "
                sqlstr += "AND w." + cattype + " IS NOT NULL "
                sqlstr += "ORDER BY rank) as t1, PickTypePoints pts "
                sqlstr += "WHERE "
                sqlstr += "pts.pick_type_id = " + str(i) + " "
                sqlstr += "AND t1.rank = pts.rank"
                session.execute(sqlstr)
                session.commit()

            elif i == 8:
                sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, update_date, points_earned) "
                sqlstr += "SELECT t1.pick_id as pick_id, t1.season as season, t1.update_date as update_date, (pts.points*t1.multiplier*t1.changed) as points_earned "
                sqlstr += "FROM "
                sqlstr += "(SELECT DISTINCT p.pick_id, p.user_id, p.multiplier, IF(p.changed=1,0.5,1) as changed, p.player_id, "
                sqlstr += "(SELECT count(*) from WeeklyMLBPlayerStats as w2, ActiveMLBPlayers as ap, "
                sqlstr += "TeamInfo as t, WeeklyTeamStats as wt  "
                sqlstr += "WHERE "
                sqlstr += "w2.update_date = '" + str(last_update) + "' "
                sqlstr += "AND w." + cattype + " IS NOT NULL "
                sqlstr += "AND w." + cattype + " <> 0 "
                sqlstr += "AND w2.season = " + str(season) + " "
                sqlstr += "AND ap.season = w2.season "
                sqlstr += "AND w2.player_id = ap.player_id "
                sqlstr += "AND ap.team_id = t.team_id "
                sqlstr += "AND ap.team_id = wt.team_id "
                sqlstr += "AND w2.innings_pitched >= wt.team_games_played "
                sqlstr += "AND wt.update_date = '" + str(last_update) + "' "
                sqlstr += "AND t.league_id = " + str(league) + " "
                sqlstr += "AND w2." + cattype + "<w." + cattype + ")+1 as rank, "
                sqlstr += "w.update_date, "
                sqlstr += "w.season "
                sqlstr += "FROM WeeklyMLBPlayerStats w, PlayerPicks p, WeeklyTeamStats wt2, ActiveMLBPlayers ap2 "
                sqlstr += "WHERE w.player_id = p.player_id "
                sqlstr += "AND ap2.player_id=p.player_id "
                sqlstr += "AND ap2.team_id = wt2.team_id "
                sqlstr += "AND w.innings_pitched >= wt2.team_games_played "
                sqlstr += "AND w.season = " + str(season) + " "
                sqlstr += "AND w.update_date = '" + str(last_update) + "' "
                sqlstr += "AND p.pick_type = " + str(i) + " "
                sqlstr += "AND p.league_id = " + str(league) + " "
                sqlstr += "AND w." + cattype + " IS NOT NULL "
                sqlstr += "AND w." + cattype + "<>0 "
                sqlstr += "ORDER BY rank) as t1, PickTypePoints pts "
                sqlstr += "WHERE "
                sqlstr += "pts.pick_type_id = " + str(i) + " "
                sqlstr += "AND t1.rank = pts.rank"
                session.execute(sqlstr)
                session.commit()

                # print(sqlstr)

            # increment counters
            if i == 8:
                league += 1
                i = 3

            i += 1

        session.close()

    @staticmethod
    def update_team_pick_points():
        session = DbSessionFactory.create_session()

        season = get_seasons()

        # this does all type 1 points
        sqlstr = "INSERT INTO WeeklyPlayerResults(pick_id, season, update_date, points_earned) "
        sqlstr += "SELECT pp.pick_id, w.season, w.update_date, p.points * pp.multiplier* (IF(pp.changed=1,0.5,1)) as points_earned "
        sqlstr += "FROM PlayerPicks pp "
        sqlstr += "LEFT JOIN WeeklyTeamStats w on pp.rank=w.division_rank and pp.team_id=w.team_id "
        sqlstr += "LEFT JOIN TeamInfo t on pp.team_id= t.team_id "
        sqlstr += "LEFT JOIN PickTypePoints p on pp.pick_type = p.pick_type_id "
        sqlstr += "WHERE pp.pick_type = 1 "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyTeamStats WHERE season = "
            + str(season)
            + ") "
        )
        sqlstr += "AND pp.league_id = t.league_id "
        sqlstr += "AND pp.division_id = t.division_id "
        sqlstr += "AND p.rank = w.division_rank "
        sqlstr += "ORDER BY pp.user_id"

        session.execute(sqlstr)
        session.commit()

        # type 2 team loss points:
        sqlstr = "INSERT INTO WeeklyPlayerResults(pick_id, season, update_date, points_earned) "
        sqlstr += "SELECT pp.pick_id, w.season, w.update_date, p.points * pp.multiplier * (IF(pp.changed=1, 0.5, 1)) as points_earned "
        sqlstr += (
            "FROM PlayerPicks pp LEFT JOIN WeeklyTeamStats w on pp.team_id = w.team_id "
        )
        sqlstr += "LEFT JOIN PickTypePoints p on pp.pick_type = p.pick_type_id "
        sqlstr += "WHERE pp.pick_type = 2 "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyTeamStats WHERE season = "
            + str(season)
            + ") "
        )
        sqlstr += "AND w.league_rank = 15"

        session.execute(sqlstr)
        session.commit()

        # type 3 team wins points:
        sqlstr = "INSERT INTO WeeklyPlayerResults(pick_id, season, update_date, points_earned) "
        sqlstr += "SELECT pp.pick_id, w.season, w.update_date, p.points * pp.multiplier * (IF(pp.changed=1, 0.5, 1)) as points_earned "
        sqlstr += (
            "FROM PlayerPicks pp LEFT JOIN WeeklyTeamStats w on pp.team_id = w.team_id "
        )
        sqlstr += "LEFT JOIN PickTypePoints p on pp.pick_type = p.pick_type_id "
        sqlstr += "WHERE pp.pick_type = 3 "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyTeamStats WHERE season = "
            + str(season)
            + ") "
        )
        sqlstr += "AND w.league_rank = 1"

        session.execute(sqlstr)
        session.commit()

        # type 9 points - wildcard - (rank 4,5 - NFLPool was 5,6)
        sqlstr = "INSERT INTO WeeklyPlayerResults (pick_id, season, update_date, points_earned) "
        sqlstr += "SELECT p.pick_id, w.season, w.update_date, pts.points*p.multiplier*IF(p.changed=1,0.5,1) as points_earned from PlayerPicks p, WeeklyTeamStats w, PickTypePoints pts "
        sqlstr += "WHERE p.pick_type = 9 "
        sqlstr += "AND p.pick_type = pts.pick_type_id "
        sqlstr += "AND w.league_rank in (4,5) "
        sqlstr += "AND w.team_id = p.team_id "
        sqlstr += "AND pts.rank = p.rank "
        sqlstr += "AND w.season = " + str(season) + " "
        sqlstr += (
            "AND w.update_date = (SELECT MAX(update_date) from WeeklyMLBPlayerStats WHERE season = "
            + str(season)
            + ") "
        )

        session.execute(sqlstr)
        session.commit()

        session.close()

    @staticmethod
    def all_seasons_played():
        """This method is used to get a list of all seasons played and display on the Standings index page
        for players to click through to see the season standings / points scored by player"""
        session = DbSessionFactory.create_session()

        seasons_played = (
            session.query(PlayerPicks.season)
            .distinct(PlayerPicks.season)
            .order_by(PlayerPicks.season.desc())
        )

        session.close()

        return seasons_played

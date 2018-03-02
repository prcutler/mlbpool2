from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.picktypes import PickTypes
from mlbpool.data.teaminfo import TeamInfo
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.services.time_service import TimeService
from mlbpool.services.gameday_service import GameDayService


class UniquePicksService:

    @classmethod
    def unique_team_picks(cls, pick_type, league=None, div=None, rank=None):
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        current_season = season_row.current_season

        now_time = TimeService.get_time()

        # Calculate Unique Picks at season start
        if now_time < GameDayService.all_star_game_date():

            txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE team_id IN "
            txtstr += "(SELECT team_id FROM (select DISTINCT(team_id), COUNT(team_id) AS ct FROM PlayerPicks WHERE "
            midstr = " GROUP BY team_id)PlayerPicks WHERE ct=1) "

            condstr = "pick_type=" + str(pick_type) + " AND season=" + str(current_season)

            if league is not None:
                condstr += " AND league_id=" + str(league)
                if div is not None:
                    condstr += " AND division_id=" + str(div)
                    if rank is not None:
                        condstr += " AND rank=" + str(rank)

            txtstr += condstr + midstr + "AND " + condstr

            # print(txtstr)

            session.execute(txtstr)
            session.commit()

        else:

            # TODO Add the changed=1 column to the query below AND give players half the point value for changed picks

            txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE team_id IN "
            txtstr += "(SELECT team_id FROM (select DISTINCT(team_id), COUNT(team_id) AS ct FROM PlayerPicks WHERE "
            midstr = " GROUP BY team_id)PlayerPicks WHERE ct=1) "

            condstr = "pick_type=" + str(pick_type) + " AND season=" + str(current_season)

            if league is not None:
                condstr += " AND league_id=" + str(league)
                if div is not None:
                    condstr += " AND division_id=" + str(div)
                    if rank is not None:
                        condstr += " AND rank=" + str(rank)

            txtstr += condstr + midstr + "AND " + condstr

            # print(txtstr)

            session.execute(txtstr)
            session.commit()

        session.close()

    @classmethod
    def unique_player_picks(cls, pick_type, league):
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        current_season = season_row.current_season

        now_time = TimeService.get_time()

        # Calculate Unique Picks at season start
        if now_time < GameDayService.all_star_game_date():

            # TODO Add if / else statement depending on what the date is and modify the query to look at changed column

            txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE player_id IN "
            txtstr += "(SELECT player_id FROM (select DISTINCT(player_id), COUNT(player_id) AS ct FROM PlayerPicks WHERE "
            midstr = " GROUP BY player_id)PlayerPicks WHERE ct=1) "

            condstr = " pick_type=" + str(pick_type) + " AND season=" + str(current_season)

            condstr += " AND league_id=" + str(league)

            txtstr += condstr + midstr + "AND " + condstr

            # print(txtstr)

            session.execute(txtstr)
            session.commit()

        else:

            # TODO Add the changed=1 column to the query below AND give players half the point value for changed picks

            txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE player_id IN "
            txtstr += "(SELECT player_id FROM (select DISTINCT(player_id), COUNT(player_id) AS ct FROM PlayerPicks WHERE "
            midstr = " GROUP BY player_id)PlayerPicks WHERE ct=1) "

            condstr = " pick_type=" + str(pick_type) + " AND season=" + str(current_season)

            condstr += " AND league_id=" + str(league)

            txtstr += condstr + midstr + "AND " + condstr

            # print(txtstr)

            session.execute(txtstr)
            session.commit()

        session.close()


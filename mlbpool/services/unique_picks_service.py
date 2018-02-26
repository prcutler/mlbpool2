from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.picktypes import PickTypes
from mlbpool.data.teaminfo import TeamInfo
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.seasoninfo import SeasonInfo


class UniquePicksService:

    @classmethod
    def unique_team_picks(cls, pick_type, league=None, div=None, rank=None):
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        current_season = season_row.current_season

        txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE team_id IN "
        txtstr += "(SELECT team_id FROM (select DISTINCT(team_id), COUNT(team_id) AS ct FROM PlayerPicks WHERE "
        midstr = " GROUP BY team_id) WHERE ct=1) "

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
    def unique_player_picks(cls, pick_type, conf):
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo).filter(SeasonInfo.id == '1').first()
        current_season = season_row.current_season

        txtstr = "UPDATE PlayerPicks SET multiplier=2 WHERE player_id IN "
        txtstr += "(SELECT player_id FROM (select DISTINCT(player_id), COUNT(player_id) AS ct FROM PlayerPicks WHERE "
        midstr = " GROUP BY player_id) WHERE ct=1) "

        condstr = " pick_type=" + str(pick_type) + " AND season=" + str(current_season)

        condstr += " AND league_id=" + str(conf)

        txtstr += condstr + midstr + "AND " + condstr

        # print(txtstr)

        session.execute(txtstr)
        session.commit()
        session.close()


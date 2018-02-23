from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.teaminfo import TeamInfo
from mlbpool.data.activeplayers import ActiveMLBPlayers
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.player_picks import PlayerPicks
import datetime
from mlbpool.services.gameday_service import GameDayService
import pendulum
from mlbpool.services.count_service import CountService


class PlayerPicksService:
    """This class displays all of the drop down menus for the different picks pool players can make in
    submit_picks.pt"""

    @staticmethod
    def get_division_team_list(league_id, division_id):
        """Get a list of the five teams in a specific division in one of the two leagues (AL or NL)"""
        session = DbSessionFactory.create_session()

        division_team_list = session.query(TeamInfo).filter(TeamInfo.league_id == league_id) \
            .filter(TeamInfo.division_id == division_id).order_by(TeamInfo.name).all()

        return division_team_list

    @staticmethod
    def get_hitter_list(league_id, position):
        """Get a list of all players who are not pitchers"""
        session = DbSessionFactory.create_session()

        player_list = session.query(ActiveMLBPlayers.player_id, ActiveMLBPlayers.firstname, ActiveMLBPlayers.lastname,
                                    ActiveMLBPlayers.position, TeamInfo.team_abbr). \
            join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id) \
            .filter(TeamInfo.league_id == league_id) \
            .filter(ActiveMLBPlayers.position != position) \
            .filter(ActiveMLBPlayers.season == SeasonInfo.current_season) \
            .order_by(ActiveMLBPlayers.lastname).all()

        return player_list

    @staticmethod
    def get_pitcher_list(league_id, position):
        """Get a list of all pitchers"""
        session = DbSessionFactory.create_session()

        player_list = session.query(ActiveMLBPlayers.player_id, ActiveMLBPlayers.firstname, ActiveMLBPlayers.lastname,
                                    ActiveMLBPlayers.position, TeamInfo.team_abbr). \
            join(TeamInfo, ActiveMLBPlayers.team_id == TeamInfo.team_id) \
            .filter(TeamInfo.league_id == league_id) \
            .filter(ActiveMLBPlayers.position == position) \
            .filter(ActiveMLBPlayers.season == SeasonInfo.current_season) \
            .order_by(ActiveMLBPlayers.lastname).all()

        return player_list

    @staticmethod
    def get_al_wildcard():
        """Get a list of all American League teams for players to choose the wildcard winners"""
        session = DbSessionFactory.create_session()

        al_wildcard_list = session.query(TeamInfo).filter(TeamInfo.league_id == 0).order_by(TeamInfo.name).all()

        return al_wildcard_list

    @staticmethod
    def get_nl_wildcard():
        """Get a list of all National League teams for players to choose the wildcard winners"""
        session = DbSessionFactory.create_session()

        nl_wildcard_list = session.query(TeamInfo).filter(TeamInfo.league_id == 1).order_by(TeamInfo.name).all()

        return nl_wildcard_list

    @staticmethod
    def get_current_season():
        """Get the current season from the SeasonInfo table"""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season

        return season

    @classmethod
    def get_player_picks(cls, al_east_winner_pick: int, al_east_second: int, al_east_last: int,
                         al_central_winner_pick: int, al_central_second: int, al_central_last: int,
                         al_west_winner_pick: int, al_west_second: int, al_west_last: int,
                         nl_east_winner_pick: int, nl_east_second: int, nl_east_last: int,
                         nl_central_winner_pick: int, nl_central_second: int, nl_central_last: int,
                         nl_west_winner_pick: int, nl_west_second: int, nl_west_last: int,
                         al_hr_pick: int, nl_hr_pick: int, al_rbi_pick: int, nl_rbi_pick: int,
                         al_ba_pick: int, nl_ba_pick: int,
                         al_p_wins_pick: int, nl_p_wins_pick: int,
                         al_era_pick: int, nl_era_pick: int,
                         al_wildcard1_pick: int, al_wildcard2_pick: int,
                         nl_wildcard1_pick: int, nl_wildcard2_pick: int,
                         al_wins_pick: int, nl_wins_pick: int,
                         al_losses_pick: int, nl_losses_pick: int,
                         twins_wins_pick: int,
                         user_id: str):

        """Get the list of selections from the POST and insert into the database"""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season

        dt = datetime.datetime.now()

        # Add American League team picks
        al_east_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=1,
                                        rank=1, team_id=al_east_winner_pick, pick_type=1,
                                        original_pick=al_east_winner_pick)
        session.add(al_east_winner_db)
        al_east_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=1,
                                        rank=2, team_id=al_east_second, pick_type=1,
                                        original_pick=al_east_second)
        session.add(al_east_second_db)

        al_east_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=1,
                                      rank=5, team_id=al_east_last, pick_type=1,
                                      original_pick=al_east_last)

        session.add(al_east_last_db)

        al_central_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=2,
                                           rank=1, team_id=al_central_winner_pick, pick_type=1,
                                           original_pick=al_central_winner_pick)
        session.add(al_central_winner_db)
        al_central_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=2,
                                           rank=2, team_id=al_central_second, pick_type=1,
                                           original_pick=al_central_second)
        session.add(al_central_second_db)

        al_central_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=2,
                                         rank=5, team_id=al_central_last, pick_type=1,
                                         original_pick=al_central_last)

        session.add(al_central_last_db)

        al_west_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=3,
                                        rank=1, team_id=al_west_winner_pick, pick_type=1,
                                        original_pick=al_west_winner_pick)
        session.add(al_west_winner_db)
        al_west_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=3,
                                        rank=2, team_id=al_west_second, pick_type=1,
                                        original_pick=al_west_second)
        session.add(al_west_second_db)

        al_west_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=0, division_id=3,
                                      rank=5, team_id=al_west_last, pick_type=1,
                                      original_pick=al_west_last)

        session.add(al_west_last_db)

        # Add National League team picks
        nl_east_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=1,
                                        rank=1, team_id=nl_east_winner_pick, pick_type=1,
                                        original_pick=nl_east_winner_pick)
        session.add(nl_east_winner_db)
        nl_east_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=1,
                                        rank=2, team_id=nl_east_second, pick_type=1,
                                        original_pick=nl_east_second)
        session.add(nl_east_second_db)

        nl_east_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=1,
                                      rank=5, team_id=nl_east_last, pick_type=1,
                                      original_pick=nl_east_last)

        session.add(nl_east_last_db)

        nl_central_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=2,
                                           rank=1, team_id=nl_central_winner_pick, pick_type=1,
                                           original_pick=nl_central_winner_pick)
        session.add(nl_central_winner_db)
        nl_central_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=2,
                                           rank=2, team_id=nl_central_second, pick_type=1,
                                           original_pick=nl_central_second)
        session.add(nl_central_second_db)

        nl_central_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=2,
                                         rank=5, team_id=nl_central_last, pick_type=1,
                                         original_pick=nl_central_last)

        session.add(nl_central_last_db)

        nl_west_winner_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=3,
                                        rank=1, team_id=nl_west_winner_pick, pick_type=1,
                                        original_pick=nl_west_winner_pick)
        session.add(nl_west_winner_db)
        nl_west_second_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=3,
                                        rank=2, team_id=nl_west_second, pick_type=1,
                                        original_pick=nl_west_second)
        session.add(nl_west_second_db)

        nl_west_last_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, league_id=1, division_id=3,
                                      rank=5, team_id=nl_west_last, pick_type=1,
                                      original_pick=nl_west_last)

        session.add(nl_west_last_db)

        # Add American League Player Picks

        al_hr_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=al_hr_pick,
                               pick_type=4, league_id=0,
                               original_pick=al_hr_pick)
        session.add(al_hr_db)

        al_ba_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=al_ba_pick,
                               pick_type=5, league_id=0,
                               original_pick=al_ba_pick)
        session.add(al_ba_db)

        al_rbi_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=al_rbi_pick,
                                pick_type=6, league_id=0, original_pick=al_rbi_pick)
        session.add(al_rbi_db)

        al_p_wins_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=al_p_wins_pick,
                                   pick_type=7, league_id=0, original_pick=al_p_wins_pick)
        session.add(al_p_wins_db)

        al_era_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=al_era_pick,
                                pick_type=8, league_id=0, original_pick=al_era_pick)
        session.add(al_era_db)

        # Add National League Player Picks

        nl_hr_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=nl_hr_pick,
                               pick_type=4, league_id=1, original_pick=nl_hr_pick)
        session.add(nl_hr_db)

        nl_ba_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=nl_ba_pick,
                               pick_type=5, league_id=1, original_pick=nl_ba_pick)
        session.add(nl_ba_db)

        nl_rbi_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=nl_rbi_pick,
                                pick_type=6, league_id=1, original_pick=nl_rbi_pick)
        session.add(nl_rbi_db)

        nl_p_wins_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=nl_p_wins_pick,
                                   pick_type=7, league_id=1, original_pick=nl_p_wins_pick)
        session.add(nl_p_wins_db)

        nl_era_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, player_id=nl_era_pick,
                                pick_type=8, league_id=1, original_pick=nl_era_pick)
        session.add(nl_era_db)

        # Add the wildcard picks
        al_wildcard1_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=al_wildcard1_pick,
                                      pick_type=9, league_id=0, original_pick=al_wildcard1_pick, rank=1)
        session.add(al_wildcard1_db)

        al_wildcard2_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=al_wildcard2_pick,
                                      pick_type=9, league_id=0, original_pick=al_wildcard2_pick, rank=2)
        session.add(al_wildcard2_db)

        nl_wildcard1_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=nl_wildcard1_pick,
                                      pick_type=9, league_id=1, original_pick=nl_wildcard1_pick, rank=1)
        session.add(nl_wildcard1_db)

        nl_wildcard2_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=nl_wildcard2_pick,
                                      pick_type=9, league_id=1, original_pick=nl_wildcard2_pick, rank=2)
        session.add(nl_wildcard2_db)

        # Add the Most Wins 
        al_wins_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=al_wins_pick,
                                 pick_type=3, league_id=0, original_pick=al_wins_pick)
        session.add(al_wins_db)

        nl_wins_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=nl_wins_pick,
                                 pick_type=3, league_id=1, original_pick=nl_wins_pick)
        session.add(nl_wins_db)

        # Add the Most Losses
        al_losses_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=al_losses_pick,
                                pick_type=2, league_id=0, original_pick=al_losses_pick)
        session.add(al_losses_db)

        nl_losses_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, team_id=nl_losses_pick,
                                pick_type=2, league_id=1, original_pick=nl_losses_pick)
        session.add(nl_losses_db)

        # Add the tiebreaker
        twins_wins_db = PlayerPicks(user_id=user_id, season=season, date_submitted=dt, twins_wins=twins_wins_pick,
                                    pick_type=10, original_pick=twins_wins_pick)
        session.add(twins_wins_db)
        session.commit()
        session.close()

    @classmethod
    def change_player_picks(cls, al_east_winner_pick: int, al_east_second_pick: int, al_east_last_pick: int,
                            al_central_winner_pick: int, al_central_second_pick: int, al_central_last_pick: int,
                            al_west_winner_pick: int, al_west_second_pick: int, al_west_last_pick: int,
                            nl_east_winner_pick: int, nl_east_second_pick: int, nl_east_last_pick: int,
                            nl_central_winner_pick: int, nl_central_second_pick: int, nl_central_last_pick: int,
                            nl_west_winner_pick: int, nl_west_second_pick: int, nl_west_last_pick: int,
                            al_hr_pick: int, nl_hr_pick: int,
                            al_rbi_pick: int, nl_rbi_pick: int,
                            al_ba_pick: int, nl_ba_pick: int,
                            al_p_wins_pick: int, nl_p_wins_pick: int,
                            al_era_pick: int, nl_era_pick: int,
                            al_wildcard1_pick: int, al_wildcard2_pick: int,
                            nl_wildcard1_pick: int, nl_wildcard2_pick: int,
                            al_wins_pick: int, nl_wins_pick: int,
                            al_losses_pick: int, nl_losses_pick: int,
                            user_id: str):

        """Update the player_picks table with the changes the pool player wants to make.
        Sets changed column to 0 (from 1) if the pick has been changed."""
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season

        dt = datetime.datetime.now()

        """If the season has not started yet, changed picks should remain 0.  If it's after the All-Star Break 
        changed should be 1.  UniquePicksService will then assign it half points.  Also, if the season has not 
        started need to update the original_pick column (which is not done at the All-Star break)"""

        # Change now_time for testing
        # Use this one for production:
        # now_time = pendulum.now(tz=pendulum.timezone('America/New_York'))
        # Use this one for testing:
        now_time = pendulum.create(2018, 7, 17, 18, 59, tz='America/New_York')
        print("Season opener date:", GameDayService.season_opener_date(), "Now time", now_time)

        if GameDayService.season_opener_date() > now_time:
            """Update the picks passed from change-picks.  If the season start date is later than the current time, 
            make the new changed picks equal to the original picks, making original_pick equal to the new pick."""

            # Update Pick Type 1
            # Update the AL East Winner Pick - check to see if it has been changed
            if al_east_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id).filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1) \
                    .update({"team_id": al_east_winner_pick, "date_submitted": dt,
                             "original_pick": al_east_winner_pick})

            # Update the AL East 2nd Place Team
            if al_east_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1). \
                    filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 1) \
                    .update({"team_id": al_east_second_pick, "date_submitted": dt,
                             "original_pick": al_east_second_pick})

            # Update the AL East Last Place Pick
            if al_east_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1). \
                    filter(PlayerPicks.rank == 5)\
                    .filter(PlayerPicks.league_id == 0).filter(
                    PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 1) \
                    .update({"team_id": al_east_last_pick, "date_submitted": dt, "original_pick": al_east_last_pick})

            # Update the AL Central Winner Pick - check to see if it has been changed
            if al_central_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1). \
                    filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update({"team_id": al_central_winner_pick, "date_submitted": dt,
                             "original_pick": al_central_winner_pick})

            # Update the AL Central 2nd Place Team
            if al_central_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update({"team_id": al_central_second_pick, "date_submitted": dt,
                             "original_pick": al_central_second_pick})

            # Update the AL Central Last Place Team
            if al_central_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1). \
                    filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update(
                    {"team_id": al_central_last_pick, "date_submitted": dt, "original_pick": al_central_last_pick})

            # Update the AL West Winner Pick - check to see if it has been changed
            if al_west_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update({"team_id": al_west_winner_pick, "date_submitted": dt,
                             "original_pick": al_west_winner_pick})

            # Update the AL West 2nd Place Team
            if al_west_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id).filter(
                    PlayerPicks.pick_type == 1). \
                    filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update({"team_id": al_west_second_pick, "date_submitted": dt,
                             "original_pick": al_west_second_pick})

            if al_west_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update(
                    {"team_id": al_west_last_pick, "date_submitted": dt, "original_pick": al_west_last_pick})

            # Update the NL East Winner Pick - check to see if it has been changed
            if nl_east_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 1) \
                    .update({"team_id": nl_east_winner_pick, "date_submitted": dt,
                             "original_pick": nl_east_winner_pick})

            # Update the NL East 2nd Place Team
            if nl_east_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 1) \
                    .update({"team_id": nl_east_second_pick, "date_submitted": dt,
                             "original_pick": nl_east_second_pick})

            # Update the NL East Last Place Pick
            if nl_east_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 1) \
                    .update(
                    {"team_id": nl_east_last_pick, "date_submitted": dt, "original_pick": nl_east_last_pick})

            # Update the NL Central Winner Pick - check to see if it has been changed
            if nl_central_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update({"team_id": nl_central_winner_pick, "date_submitted": dt,
                             "original_pick": nl_central_winner_pick})

            # Update the NL Central 2nd Place Team
            if nl_central_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update({"team_id": nl_central_second_pick, "date_submitted": dt,
                             "original_pick": nl_central_second_pick})

            if nl_central_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 2) \
                    .update(
                    {"team_id": nl_central_last_pick, "date_submitted": dt, "original_pick": nl_central_last_pick})

            # Update the NL West Winner Pick - check to see if it has been changed
            if nl_west_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1)\
                    .filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update({"team_id": nl_west_winner_pick, "date_submitted": dt,
                             "original_pick": nl_west_winner_pick})

            # Update the NL West 2nd Place Team
            if nl_west_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2)\
                    .filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update({"team_id": nl_west_second_pick, "date_submitted": dt,
                             "original_pick": nl_west_second_pick})

            # Update the NL West Last Place Team
            if nl_west_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 3):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1)\
                    .filter(PlayerPicks.division_id == 3) \
                    .update(
                    {"team_id": nl_west_last_pick, "date_submitted": dt, "original_pick": nl_west_last_pick})

            # Update Pick Type 2 - Team Losses
            if al_losses_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id)\
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 2)\
                    .filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.team_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id)\
                    .filter(PlayerPicks.pick_type == 2)\
                    .filter(PlayerPicks.league_id == 0)\
                    .update({"team_id": al_losses_pick, "date_submitted": dt, "original_pick": al_losses_pick})

            if nl_losses_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id)\
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 2)\
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id)\
                    .filter(PlayerPicks.pick_type == 2)\
                    .filter(PlayerPicks.league_id == 1)\
                    .update({"team_id": nl_losses_pick, "date_submitted": dt, "original_pick": nl_losses_pick})

            # Update Pick Type 3 - Team Wins
            if al_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.team_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"team_id": al_wins_pick, "date_submitted": dt, "original_pick": al_wins_pick})

            if nl_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"team_id": nl_wins_pick, "date_submitted": dt, "original_pick": nl_wins_pick})

            # Update Pick Type 4 - Home Runs
            if al_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_hr_pick, "date_submitted": dt, "original_pick": al_hr_pick})

            if nl_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_hr_pick, "date_submitted": dt, "original_pick": nl_hr_pick})

            # Update Pick Type 5 - Batting Average
            if al_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_ba_pick, "date_submitted": dt, "original_pick": al_ba_pick})

            if nl_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_ba_pick, "date_submitted": dt, "original_pick": nl_ba_pick})

            # Update Pick Type 6 - RBIs
            if al_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_rbi_pick, "date_submitted": dt, "original_pick": al_rbi_pick})

            if nl_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_rbi_pick, "date_submitted": dt, "original_pick": nl_rbi_pick})

            # Update Pick Type 7 - Pitcher Wins
            if al_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_p_wins_pick, "date_submitted": dt, "original_pick": al_p_wins_pick})

            if nl_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_p_wins_pick, "date_submitted": dt, "original_pick": nl_p_wins_pick})

            # Update Pick Type 8 - ERA
            if al_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_era_pick, "date_submitted": dt, "original_pick": al_era_pick})

            if nl_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_era_pick, "date_submitted": dt, "original_pick": nl_era_pick})

            # Update Pick Type 9 - Wildcard Teams
            if al_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"team_id": al_wildcard1_pick, "date_submitted": dt, "original_pick": al_wildcard1_pick})

            if al_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.team_id)\
                    .filter(PlayerPicks.rank == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"team_id": al_wildcard2_pick, "date_submitted": dt, "original_pick": al_wildcard2_pick})

            if nl_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"team_id": nl_wildcard1_pick, "date_submitted": dt, "original_pick": nl_wildcard1_pick})

            if nl_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"team_id": nl_wildcard2_pick, "date_submitted": dt, "original_pick": nl_wildcard2_pick})

        else:
            """If the season has started, update picks at the All-Star Break.  Do not change the original pick column
            and update the changed column to 1."""

            # Update the AL East Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(al_east_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": al_east_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_east_winner_pick)

            # Update the AL East 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(al_east_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": al_east_winner_pick, "date_submitted": dt, "changed": 1})

                    print("Original pick:", pick, type(pick), "New picK:", al_east_second_pick)

            # Update the AL East Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(al_east_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": al_east_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_east_last_pick)

            # Update the AL Central Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(al_central_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_central_winner_pick)

            # Update the AL Central 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(al_central_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

                    print("Original pick:", pick, type(pick), "New picK:", al_central_second_pick)

            # Update the AL Central Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(al_central_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_central_last_pick)

            # Update the AL West Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(al_central_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_central_winner_pick)

            # Update the AL West 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id)\
                    .filter(PlayerPicks.season == season)\
                    .filter(PlayerPicks.pick_type == 1)\
                    .filter(PlayerPicks.rank == 2)\
                    .filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(al_central_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

#            print("Original pick:", pick, type(pick), "New picK:", al_central_second_pick)

            # Update the AL West Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(al_central_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 0) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": al_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", al_central_last_pick)

            # Update the NL East Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(nl_east_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": nl_east_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", nl_east_winner_pick)

            # Update the NL East 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(nl_east_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": nl_east_winner_pick, "date_submitted": dt, "changed": 1})

#                print("Original pick:", pick, type(pick), "New picK:", nl_east_second_pick)

            # Update the NL East Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 1).first():

                if pick != int(nl_east_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 1) \
                        .update({"team_id": nl_east_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", nl_east_last_pick)

            # Update the NL Central Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(nl_central_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", nl_central_winner_pick)

            # Update the NL Central 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(nl_central_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

                    print("Original pick:", pick, type(pick), "New picK:", nl_central_second_pick)

            # Update the NL Central Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 2).first():

                if pick != int(nl_central_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 2) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", nl_central_last_pick)

            # Update the NL West Winner Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(nl_central_winner_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 1).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

#                    print("Original pick:", pick, type(pick), "New picK:", nl_central_winner_pick)

            # Update the NL West 2nd Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(nl_central_second_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 2).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

#            print("Original pick:", pick, type(pick), "New picK:", nl_central_second_pick)

            # Update the NL West Last Place Team
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.division_id == 3).first():

                if pick != int(nl_central_last_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 1) \
                        .filter(PlayerPicks.rank == 5).filter(PlayerPicks.league_id == 1) \
                        .filter(PlayerPicks.division_id == 3) \
                        .update({"team_id": nl_central_winner_pick, "date_submitted": dt, "changed": 1})

#                print("Original pick:", pick, type(pick), "New picK:", nl_central_last_pick)

            # Update Pick Type 2 - Team Losses
            # Update the AL Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 2) \
                    .filter(PlayerPicks.league_id == 0).first():

                if pick != int(al_losses_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 2) \
                        .filter(PlayerPicks.league_id == 0)\
                        .update({"team_id": al_losses_pick, "date_submitted": dt, "changed": 1})

            # Update the NL Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 2) \
                    .filter(PlayerPicks.league_id == 1).first():

                if pick != int(nl_losses_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 2) \
                        .filter(PlayerPicks.league_id == 1) \
                        .update({"team_id": nl_losses_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 3 - Team Wins
            # Update the AL Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 0).first():

                if pick != int(al_wins_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 3) \
                        .filter(PlayerPicks.league_id == 0) \
                        .update({"team_id": al_wins_pick, "date_submitted": dt, "changed": 1})

            # Update the NL Pick
            for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 3) \
                    .filter(PlayerPicks.league_id == 1).first():

                if pick != int(nl_wins_pick):
                    session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                        .filter(PlayerPicks.pick_type == 3) \
                        .filter(PlayerPicks.league_id == 1) \
                        .update({"team_id": nl_wins_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 4 - Home Runs
            if al_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_hr_pick, "date_submitted": dt, "changed": 1})

            if nl_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 4) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_hr_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 5 - Batting Average
            if al_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_ba_pick, "date_submitted": dt, "changed": 1})

            if nl_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 5) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_ba_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 6 - RBIs
            if al_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_rbi_pick, "date_submitted": dt, "changed": 1})

            if nl_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 6) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_rbi_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 7 - Pitcher Wins
            if al_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_p_wins_pick, "date_submitted": dt, "changed": 1})

            if nl_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 7) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_p_wins_pick, "date_submitted": dt, "changed": 1})

            # Update Pick Type 8 - Pitcher ERA
            if al_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 0) \
                    .update(
                    {"player_id": al_era_pick, "date_submitted": dt, "changed": 1})

            if nl_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.player_id):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 8) \
                    .filter(PlayerPicks.league_id == 1) \
                    .update(
                    {"player_id": nl_era_pick, "date_submitted": dt, "changed": 1})
                
            # Update Pick Type 9 - Wildcard Teams
            if al_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.rank == 1) \
                    .update(
                    {"team_id": al_wins_pick, "date_submitted": dt, "changed": 1})

            if nl_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 1):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .update(
                    {"team_id": nl_wildcard1_pick, "date_submitted": dt, "changed": 1})

            if al_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0)\
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.rank == 2) \
                    .update(
                    {"team_id": al_wildcard2_pick, "date_submitted": dt, "changed": 1})

            if nl_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.team_id) \
                    .filter(PlayerPicks.rank == 2):
                session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.pick_type == 9) \
                    .filter(PlayerPicks.league_id == 1) \
                    .filter(PlayerPicks.rank == 2) \
                    .update(
                    {"team_id": nl_wildcard2_pick, "date_submitted": dt, "changed": 1})

        session.commit()
        session.close()


class DisplayPlayerPicks:

    @staticmethod
    def display_picks(user_id):
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season

        user_query = session.query(PlayerPicks, TeamInfo.name).join(TeamInfo, PlayerPicks.team_id == TeamInfo.team_id) \
            .filter(PlayerPicks.user_id == user_id) \
            .filter(PlayerPicks.season == season).all()

        #        print(user_query)
        #        print(type(user_query[0]))

        session.close()
        return user_query



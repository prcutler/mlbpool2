from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks


class CountService:

    @staticmethod
    def change_picks_count(user_id, season, al_east_winner_pick, al_east_second_pick, al_east_last_pick,
                           al_central_winner_pick, al_central_second_pick, al_central_last_pick,
                           al_west_winner_pick, al_west_second_pick, al_west_last_pick,
                           nl_east_winner_pick, nl_east_second_pick, nl_east_last_pick,
                           nl_central_winner_pick, nl_central_second_pick, nl_central_last_pick,
                           nl_west_winner_pick, nl_west_second_pick, nl_west_last_pick,
                           al_losses_pick, nl_losses_pick, al_wins_pick, nl_wins_pick,
                           al_hr_pick, nl_hr_pick, al_ba_pick, nl_ba_pick,
                           al_rbi_pick, nl_rbi_pick,
                           al_p_wins_pick, nl_p_wins_pick,
                           al_era_pick, nl_era_pick,
                           al_wildcard1_pick, nl_wildcard1_pick,
                           al_wildcard2_pick, nl_wildcard2_pick):

        picks_changed = 0

        session = DbSessionFactory.create_session()

        # Update the AL East Winner Pick
        if al_east_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1):

            picks_changed += 1

        # Update the AL East 2nd Place Team
        if al_east_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1):

            picks_changed += 1

        # Update the AL East Last Place Team
        if al_east_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1):

            picks_changed += 1

        # Update the AL Central Winner Pick
        if al_central_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the AL Central 2nd Place Team
        if al_central_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the AL Central Last Place Team
        if al_central_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the AL West Winner Pick
        if al_west_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update the AL West 2nd Place Team
        if al_west_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update the AL West Last Place Team
        if al_west_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update the NL East Winner Pick
        if nl_east_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1):
            picks_changed += 1

        # Update the NL East 2nd Place Team
        if nl_east_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1):
            picks_changed += 1

        # Update the NL East Last Place Team
        if nl_east_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1):
            picks_changed += 1

        # Update the NL Central Winner Pick
        if nl_central_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the NL Central 2nd Place Team
        if nl_central_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the NL Central Last Place Team
        if nl_central_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 2):
            picks_changed += 1

        # Update the NL West Winner Pick
        if nl_west_winner_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update the NL West 2nd Place Team
        if nl_west_second_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update the NL West Last Place Team
        if nl_west_last_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 3) \
                .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 3):
            picks_changed += 1

        # Update Pick Type 2 - Team Losses
        if al_losses_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id):
            picks_changed += 1

        if nl_losses_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id):
            picks_changed += 1

        # Update Pick Type 3 - Team Wins
        if al_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 3) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id):
            picks_changed += 1

        if nl_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 3) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id):
            picks_changed += 1

        # Update Pick Type 4 - Home Runs
        if al_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 4) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        if nl_hr_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 4) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        # Update Pick Type 5 - Batting Average
        if al_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 5) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        if nl_ba_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 5) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        # Update Pick Type 6 - RBIs
        if al_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 6) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        if nl_rbi_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 6) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        # Update Pick Type 7 - Pitcher Wins
        if al_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 7) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        if nl_p_wins_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 7) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        # Update Pick Type 8 - Pitcher ERA
        if al_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 8) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        if nl_era_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 8) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id):
            picks_changed += 1

        # Update Pick Type 9 - Wildcard Teams
        if al_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 1):
            picks_changed += 1

        if nl_wildcard1_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 1):
            picks_changed += 1

        if al_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 2):
            picks_changed += 1

        if nl_wildcard2_pick != session.query(PlayerPicks).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 2):
            picks_changed += 1

        session.close()

        return picks_changed


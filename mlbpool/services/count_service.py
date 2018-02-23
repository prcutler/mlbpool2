from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.seasoninfo import SeasonInfo


class CountService:

    @staticmethod
    def find_changes(user_id):
        session = DbSessionFactory.create_session()

        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == 1).first()
        season = season_row.current_season

        try:
            for pick in session.query(PlayerPicks.changed).filter(PlayerPicks.user_id == user_id) \
                    .filter(PlayerPicks.season == season) \
                    .filter(PlayerPicks.pick_type == 1) \
                    .filter(PlayerPicks.rank == 1) \
                    .filter(PlayerPicks.league_id == 0) \
                    .filter(PlayerPicks.division_id == 1).first():

                return pick

        except TypeError:

            pick = 0
            return pick

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

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1).first():

            print("Pick in DB:", pick, type(pick), "Pick from Submit:", al_east_winner_pick, type(al_east_winner_pick))
            int_pick = int(al_east_winner_pick)
            print(int_pick == pick)

            if int(al_east_winner_pick) == pick:
                picks_changed += 0
                print("No change for", al_east_winner_pick)

            else:
                picks_changed += 1
                print("This is the else statement", picks_changed, type(picks_changed), al_east_winner_pick)

        # Update the AL East 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1).first():

            if int(al_east_second_pick) == pick:
                picks_changed += 0
                print("No change for", al_east_second_pick)

            else:
                picks_changed += 1
                print(picks_changed, al_east_second_pick)

        # Update the AL East Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 1).first():

            if int(al_east_last_pick) == pick:
                picks_changed += 0
                print("No change for", al_east_last_pick)
            else:
                picks_changed += 1
                print(picks_changed, al_east_last_pick)

        # Update the AL Central Winner Pick
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 2).first():
            
            if int(al_central_winner_pick) == pick:
                picks_changed += 0
            
            else:
                picks_changed += 1
                print(picks_changed, al_central_winner_pick)

        # Update the AL Central 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 2).first():
            
            if int(al_central_second_pick) == pick:
                picks_changed += 0
            
            else:
                picks_changed += 1
                print(picks_changed, al_central_second_pick)

        # Update the AL Central Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 2).first():
            
            if int(al_central_last_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed, al_central_last_pick)

        # Update the AL West Winner Pick
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 3).first():
            
            if int(al_west_winner_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the AL West 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.division_id == 3).first():

            if int(al_west_second_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the AL West Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 0).filter(PlayerPicks.division_id == 3).first():

            if int(al_west_last_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL East Winner Pick
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1).first():

            if int(nl_east_winner_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL East 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1).first():

            if int(nl_east_second_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL East Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 1).first():

            if int(nl_east_last_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL Central Winner Pick
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 2).first():

            if int(nl_central_winner_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL Central 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 2).first():

            if int(nl_central_second_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL Central Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 2).first():

            if int(nl_central_last_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL West Winner Pick
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 1) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 3).first():

            if int(nl_west_winner_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL West 2nd Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.division_id == 3).first():

            if int(nl_west_second_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update the NL West Last Place Team
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 1) \
                .filter(PlayerPicks.rank == 5) \
                .filter(PlayerPicks.league_id == 1).filter(PlayerPicks.division_id == 3).first():

            if int(nl_west_last_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 2 - Team Losses
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 2) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id).first():

            if int(al_losses_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 2) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id).first():

            if int(nl_losses_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 3 - Team Wins
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 3) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id).first():

            if int(al_wins_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 3) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id).first():

            if int(nl_wins_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 4 - Home Runs
        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 4) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id).first():

            if int(al_hr_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 4) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id).first():

            if int(nl_hr_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 5 - Batting Average
        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 5) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id).first():

            if int(al_ba_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 5) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id).first():

            if int(nl_ba_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 6 - RBIs
        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 6) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id).first():

            if int(al_rbi_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 6) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id).first():

            if int(nl_rbi_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 7 - Pitcher Wins
        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 7) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id).first():

            if int(al_p_wins_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 7) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id).first():

            if int(nl_p_wins_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 8 - Pitcher ERA
        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 8) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.player_id).first():

            if int(al_era_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.player_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 8) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.player_id).first():

            if int(nl_era_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        # Update Pick Type 9 - Wildcard Teams
        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 1).first():

            if int(al_wildcard1_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 1).first():

            if int(nl_wildcard1_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 0) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 2).first():

            if int(al_wildcard2_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        for pick in session.query(PlayerPicks.team_id).filter(PlayerPicks.user_id == user_id) \
                .filter(PlayerPicks.season == season) \
                .filter(PlayerPicks.pick_type == 9) \
                .filter(PlayerPicks.league_id == 1) \
                .filter(PlayerPicks.team_id) \
                .filter(PlayerPicks.rank == 2).first():

            if int(nl_wildcard2_pick) == pick:
                picks_changed += 0
            else:
                picks_changed += 1
                print(picks_changed)

        session.close()

        return picks_changed


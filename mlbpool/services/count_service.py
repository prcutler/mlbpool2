from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks


class CountService:

    @staticmethod
    def change_picks_count(user_id, season, al_east_winner_pick, al_east_second_pick, al_east_last_pick):

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

        session.close()

        return picks_changed


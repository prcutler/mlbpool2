import pyramid_handlers
from mlbpool.controllers.base_controller import BaseController
from mlbpool.services.playerpicks_service import PlayerPicksService
from mlbpool.viewmodels.playerpicks_viewmodel import PlayerPicksViewModel
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.account import Account
import datetime


class PicksController(BaseController):
    @pyramid_handlers.action(renderer='templates/picks/index.pt')
    def index(self):
        if not self.logged_in_user_id:
            print("Cannot view account page, you must be logged in")
            self.redirect('/account/signin')

        return {}

    @pyramid_handlers.action(renderer='templates/picks/completed.pt')
    def completed(self):
        if not self.logged_in_user_id:
            print("Cannot view account page, you must be logged in")
            self.redirect('/account/signin')

        #        display_player_picks = DisplayPlayerPicks.display_picks(self.logged_in_user_id)

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        first_name = get_first_name[0]

        return {'season': season,
                'first_name': first_name}

    # Get player picks for the current season
    @pyramid_handlers.action(renderer='templates/picks/submit-picks.pt',
                             request_method='GET',
                             name='submit-picks')
    def submit_player_picks(self):

        if not self.logged_in_user_id:
            print("Cannot view picks page, you must be logged in")
            self.redirect('/account/signin')

        dt = datetime.datetime.now()

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        #        first_game = session.query(SeasonInfo.season_start_date).filter(SeasonInfo.current_season == season)\
        #            .filter(SeasonInfo.season_start_date).first()

        # TODO Refactor this to use Maya datetimes

        #        string_date = first_game[0] + ' 21:59'
        #        first_game_time = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M")

        #        if dt > first_game_time:
        #            print("Season has already started")
        #            self.redirect('/picks/too-late')
        #        else:

        #            if not self.logged_in_user_id:
        #                print("Cannot view account page, you must be logged in")
        #                self.redirect('/account/signin')

        # Check if user has already submitted picks
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        user_query = session.query(PlayerPicks.user_id).filter(PlayerPicks.user_id == self.logged_in_user_id) \
            .filter(PlayerPicks.season == season).first()

        if user_query is None:

            # Data / Service access
            al_east_list = PlayerPicksService.get_division_team_list(0, 1)
            al_central_list = PlayerPicksService.get_division_team_list(0, 2)
            al_west_list = PlayerPicksService.get_division_team_list(0, 3)

            nl_east_list = PlayerPicksService.get_division_team_list(1, 1)
            nl_central_list = PlayerPicksService.get_division_team_list(1, 2)
            nl_west_list = PlayerPicksService.get_division_team_list(1, 3)

            # Pass the P as the pitcher position and the query to get the list != P
            al_batter_list = PlayerPicksService.get_hitter_list(0, 'P')
            nl_batter_list = PlayerPicksService.get_hitter_list(1, 'P')

            # List of all Pitchers
            al_pitcher_list = PlayerPicksService.get_pitcher_list(0, 'P')
            nl_pitcher_list = PlayerPicksService.get_pitcher_list(1, 'P')

            # List of all teams to pick the Wild Card from each league
            al_wildcard_list = PlayerPicksService.get_al_wildcard()
            nl_wildcard_list = PlayerPicksService.get_nl_wildcard()

            # Create a range of 0-162 for players to pick how many wins the Twins will finish with
            twins_wins_pick_list = list(range(0, 163))

            # Get the user ID
            user_id = self.logged_in_user_id
            get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
                .first()
            first_name = get_first_name[0]

            # Return the models
            return {
                'season': season,
                'user_id': user_id,
                'first_name': first_name,
                'al_east': al_east_list,
                'al_central': al_central_list,
                'al_west': al_west_list,
                'nl_east': nl_east_list,
                'nl_central': nl_central_list,
                'nl_west': nl_west_list,
                'al_hitter_list': al_batter_list,
                'nl_hitter_list': nl_batter_list,
                'al_pitcher_list': al_pitcher_list,
                'nl_pitcher_list': nl_pitcher_list,
                'al_wildcard_list': al_wildcard_list,
                'nl_wildcard_list': nl_wildcard_list,
                'twins_wins_pick_list': twins_wins_pick_list
            }

        else:
            print("You have already submitted picks for this season")
            self.redirect('/picks/completed')

    # POST /picks/submit_picks
    @pyramid_handlers.action(renderer='templates/picks/submit-picks.pt',
                             request_method='POST',
                             name='submit-picks')
    def submit_player_picks_post(self):
        vm = PlayerPicksViewModel()
        vm.from_dict(self.request.POST)

        # Pass a player's picks to the service to be inserted in the db

        vm.user_id = self.logged_in_user_id

        player_picks = PlayerPicksService.get_player_picks(vm.al_east_winner_pick, vm.al_east_second_pick,
                                                           vm.al_east_last_pick,
                                                           vm.al_central_winner_pick, vm.al_central_second_pick,
                                                           vm.al_central_last_pick,
                                                           vm.al_west_winner_pick, vm.al_west_second_pick,
                                                           vm.al_west_last_pick,
                                                           vm.nl_east_winner_pick, vm.nl_east_second_pick,
                                                           vm.nl_east_last_pick,
                                                           vm.nl_central_winner_pick, vm.nl_central_second_pick,
                                                           vm.nl_central_last_pick,
                                                           vm.nl_west_winner_pick, vm.nl_west_second_pick,
                                                           vm.nl_west_last_pick,
                                                           vm.al_hr_pick, vm.nl_hr_pick,
                                                           vm.al_rbi_pick, vm.nl_rbi_pick,
                                                           vm.al_ba_pick, vm.nl_ba_pick,
                                                           vm.al_p_wins_pick, vm.nl_p_wins_pick,
                                                           vm.al_era_pick, vm.nl_era_pick,
                                                           vm.al_wildcard1_pick, vm.al_wildcard2_pick,
                                                           vm.nl_wildcard1_pick, vm.nl_wildcard2_pick,
                                                           vm.al_wins_pick, vm.nl_wins_pick,
                                                           vm.al_losses_pick, vm.nl_losses_pick,
                                                           vm.twins_wins_pick,
                                                           vm.user_id)

        # Log that a user submitted picks

    #        self.log.notice("Picks submitted by {}.".format(self.logged_in_user.email))

    # redirect
    # TODO: Create review page before database?
        self.redirect('/picks/completed')

    @pyramid_handlers.action(renderer='templates/picks/too-late.pt',
                             request_method='GET',
                             name='too-late')
    def too_late(self):
        if not self.logged_in_user_id:
            print("Cannot view account page, you must be logged in")
            self.redirect('/account/signin')

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        return {'season': season}

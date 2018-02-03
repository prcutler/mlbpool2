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

        first_game = session.query(SeasonInfo.season_start_date).filter(SeasonInfo.current_season == season)\
            .filter(SeasonInfo.season_start_date).first()

        # TODO Refactor this to use Maya datetimes

        string_date = first_game[0] + ' 21:59'
        first_game_time = datetime.datetime.strptime(string_date, "%Y-%m-%d %H:%M")

        if dt > first_game_time:
            print("Season has already started")
            self.redirect('/picks/too-late')
        else:

            if not self.logged_in_user_id:
                print("Cannot view account page, you must be logged in")
                self.redirect('/account/signin')

        # Check if user has already submitted picks
        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        print(season)

        user_query = session.query(PlayerPicks.user_id).filter(PlayerPicks.user_id == self.logged_in_user_id)\
            .filter(PlayerPicks.season == season).first()

        if user_query is None:

            # Data / Service access
            al_east_list = PlayerPicksService.get_division_team_list(0, 1)
            al_central_list = PlayerPicksService.get_division_team_list(0, 2)
            al_west_list = PlayerPicksService.get_division_team_list(0, 3)
            
            nl_east_list = PlayerPicksService.get_division_team_list(1, 1)
            nl_central_list = PlayerPicksService.get_division_team_list(1, 2)
            nl_west_list = PlayerPicksService.get_division_team_list(1, 3)

            # TODO Can I pass something like =! P?
            # List of all hitting positions (excluding pitchers)
            al_hr_list = PlayerPicksService.get_hitter_list(0, 'P')
            nl_hr_list = PlayerPicksService.get_hitter_list(1, 'P')

            al_rbi_list = PlayerPicksService.get_hitter_list(0, 'P')
            nl_rbi_list = PlayerPicksService.get_hitter_list(1, 'P')
            
            al_ba_list = PlayerPicksService.get_hitter_list(0, 'P')
            nl_ba_list = PlayerPicksService.get_hitter_list(1, 'P')

            # List of all Pitchers
            al_p_wins_list = PlayerPicksService.get_pitcher_list(0, 'P')
            nl_p_wins_list = PlayerPicksService.get_pitcher_list(1, 'P')
            
            al_era_list = PlayerPicksService.get_pitcher_list(0, 'P')
            nl_era_list = PlayerPicksService.get_pitcher_list(1, 'P')

            # List of all teams to pick the Wild Card from each league
            al_wildcard_list = PlayerPicksService.get_al_wildcard()
            nl_wildcard_list = PlayerPicksService.get_nl_wildcard()

            # TODO Write the Twins wins service

            # Get the user ID
            user_id = self.logged_in_user_id
            get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id)\
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
                'al_hr_list': al_hr_list,
                'nl_hr_list': nl_hr_list,
                'al_rbi_list': al_rbi_list,
                'nl_rbi_list': nl_rbi_list,
                'al_ba_list': al_ba_list,
                'nl_ba_list': nl_ba_list,
                'al_p_wins_list': al_p_wins_list,
                'nl_p_wins_list': nl_p_wins_list,
                'al_era_list': al_era_list,
                'nl_era_list': nl_era_list,
                'al_wildcard_list': al_wildcard_list,
                'nl_wildcard_list': nl_wildcard_list,
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

        player_picks = PlayerPicksService.get_player_picks(vm.afc_east_winner_pick, vm.afc_east_second, 
                                                           vm.afc_east_last,
                                                           vm.afc_north_winner_pick, vm.afc_north_second,
                                                           vm.afc_north_last,
                                                           vm.afc_south_winner_pick, vm.afc_south_second,
                                                           vm.afc_south_last,
                                                           vm.afc_west_winner_pick, vm.afc_west_second,
                                                           vm.afc_west_last,
                                                           vm.nfc_east_winner_pick, vm.nfc_east_second,
                                                           vm.nfc_east_last,
                                                           vm.nfc_north_winner_pick, vm.nfc_north_second,
                                                           vm.nfc_north_last,
                                                           vm.nfc_south_winner_pick, vm.nfc_south_second,
                                                           vm.nfc_south_last,
                                                           vm.nfc_west_winner_pick, vm.nfc_west_second,
                                                           vm.nfc_west_last,
                                                           vm.afc_qb_pick, vm.nfc_qb_pick,
                                                           vm.afc_rb_pick, vm.nfc_rb_pick,
                                                           vm.afc_rec_pick, vm.nfc_rec_pick,
                                                           vm.afc_sacks_pick, vm.nfc_sacks_pick,
                                                           vm.afc_int_pick, vm.nfc_int_pick,
                                                           vm.afc_wildcard1_pick, vm.afc_wildcard2_pick,
                                                           vm.nfc_wildcard1_pick, vm.nfc_wildcard2_pick,
                                                           vm.afc_pf_pick, vm.nfc_pf_pick,
                                                           vm.specialteams_td_pick,
                                                           vm.user_id)

        # Log that a user submitted picks
        self.log.notice("Picks submitted by {}.".format(self.logged_in_user.email))

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

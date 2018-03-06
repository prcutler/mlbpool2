import pyramid_handlers
from mlbpool.controllers.base_controller import BaseController
from mlbpool.services.playerpicks_service import PlayerPicksService
from mlbpool.services.view_picks_service import ViewPicksService
from mlbpool.viewmodels.playerpicks_viewmodel import PlayerPicksViewModel
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.player_picks import PlayerPicks
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.account import Account
from mlbpool.services.gameday_service import GameDayService
from mlbpool.services.count_service import CountService
from mlbpool.services.time_service import TimeService
from mlbpool.services.slack_service import SlackService


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

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        season_info = session.query(SeasonInfo).all()

        season_start_date = GameDayService.season_opener_date()
        picks_due = GameDayService.picks_due()
        time_due = GameDayService.time_due()

        # Change now_time for testing
        # Use this one for production:
        # now_time = pendulum.now(tz=pendulum.timezone('America/New_York'))
        # Use this one for testing:
        now_time = TimeService.get_time()

        # Check if the season has already started
        if now_time > season_start_date:
            print("Too late!  The season has already started.")
            self.redirect('/picks/too-late')

        else:

            days = GameDayService.delta_days()
            hours = GameDayService.delta_hours()
            minutes = GameDayService.delta_minutes()
            current_datetime = now_time.to_day_datetime_string()

            # Check if user has already submitted picks

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
                    'twins_wins_pick_list': twins_wins_pick_list,
                    'picks_due': picks_due,
                    'time_due': time_due,
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                    'current_datetime': current_datetime,
                    'season_info': season_info
                }

            else:
                print("You have already submitted picks for this season")
                self.redirect('/picks/change-picks')

            session.close()

    # POST /picks/submit_picks
    @pyramid_handlers.action(renderer='templates/picks/submit-picks.pt',
                             request_method='POST',
                             name='submit-picks')
    def submit_player_picks_post(self):
        vm = PlayerPicksViewModel()
        vm.from_dict(self.request.POST)

        # Pass a player's picks to the service to be inserted in the db

        session = DbSessionFactory.create_session()

        vm.user_id = self.logged_in_user_id
        get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        first_name = get_first_name[0]

        get_last_name = session.query(Account.last_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        last_name = get_last_name[0]

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

        self.log.notice("Picks submitted by {}.".format(self.logged_in_user.email))

        message = f'Picks submitted by MLBPool2 user:  {first_name} {last_name}'
        print(message)

        SlackService.send_message(message)

        session.close()

        # redirect
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

        session.close()

        return {'season': season}

    # Change player picks for the current season
    @pyramid_handlers.action(renderer='templates/picks/change-picks.pt',
                             request_method='GET',
                             name='change-picks')
    def change_player_picks(self):

        if not self.logged_in_user_id:
            print("Cannot view picks page, you must be logged in")
            self.redirect('/account/signin')

        # Check if user has already submitted picks

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        user_query = session.query(PlayerPicks.user_id).filter(PlayerPicks.user_id == self.logged_in_user_id) \
            .filter(PlayerPicks.season == season).first()

        find_changes = CountService.find_changes(self.logged_in_user_id)

        if user_query is None and find_changes is 0:

            print("You have not submitted picks for this season")
            self.redirect('/picks/submit-picks')

        elif find_changes == 1:
            print(find_changes)
            self.redirect('/picks/too-many')

        else:

            now_time = TimeService.get_time()

            if now_time < GameDayService.season_opener_date() and GameDayService.all_star_break(now_time) is False:

                self.redirect('/picks/too-late')

            elif now_time > GameDayService.season_opener_date() and GameDayService.all_star_break(now_time) is False:

                self.redirect('/picks/too-late')

            else:

                session = DbSessionFactory.create_session()
                season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
                season = season_row.current_season

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

                # Get the original picks the player made
                all_picks = ViewPicksService.display_picks(self.logged_in_user_id, season)

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
                    'twins_wins_pick_list': twins_wins_pick_list,
                    'all_picks': all_picks
                }

            session.close()

    # POST /picks/submit_picks
    @pyramid_handlers.action(renderer='templates/picks/change-picks.pt',
                             request_method='POST',
                             name='change-picks')
    def change_player_picks_post(self):
        vm = PlayerPicksViewModel()
        vm.from_dict(self.request.POST)

        # Pass a player's picks to the service to be inserted in the db

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season
        vm.user_id = self.logged_in_user_id
        vm.season = season

        now_time = TimeService.get_time()

        if GameDayService.season_opener_date() < now_time:
            total_changes = CountService.change_picks_count(
                vm.user_id, vm.season, vm.al_east_winner_pick, vm.al_east_second_pick, vm.al_east_last_pick,
                vm.al_central_winner_pick, vm.al_central_second_pick, vm.al_central_last_pick,
                vm.al_west_winner_pick, vm.al_west_second_pick, vm.al_west_last_pick,
                vm.nl_east_winner_pick, vm.nl_east_second_pick, vm.nl_east_last_pick,
                vm.nl_central_winner_pick, vm.nl_central_second_pick, vm.nl_central_last_pick,
                vm.nl_west_winner_pick, vm.nl_west_second_pick, vm.nl_west_last_pick,
                vm.al_losses_pick, vm.nl_losses_pick, vm.al_wins_pick, vm.nl_wins_pick,
                vm.al_hr_pick, vm.nl_hr_pick, vm.al_ba_pick, vm.nl_ba_pick,
                vm.al_rbi_pick, vm.nl_rbi_pick,
                vm.al_p_wins_pick, vm.nl_p_wins_pick,
                vm.al_era_pick, vm.nl_era_pick,
                vm.al_wildcard1_pick, vm.nl_wildcard1_pick,
                vm.al_wildcard2_pick, vm.nl_wildcard2_pick)

            #            print(now_time, total_changes, "Why is this not working?")

            if total_changes >= 13:
                self.redirect('/picks/too-many')

            else:

                PlayerPicksService.change_player_picks(vm.al_east_winner_pick, vm.al_east_second_pick,
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
                                                       vm.user_id)
        else:

            PlayerPicksService.change_player_picks(vm.al_east_winner_pick, vm.al_east_second_pick,
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
                                                   vm.user_id)

        # Log that a user changed picks

        self.log.notice("Picks changed by {}.".format(self.logged_in_user.email))

        get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        first_name = get_first_name[0]

        get_last_name = session.query(Account.last_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        last_name = get_last_name[0]

        message = f'Picks updated by MLBPool2 user:  {first_name} {last_name}'
        print(message)

        SlackService.send_message(message)

        session.close()

        # redirect
        self.redirect('/account')

    @pyramid_handlers.action(renderer='templates/picks/too-many.pt',
                             request_method='GET',
                             name='too-many')
    def too_many(self):
        if not self.logged_in_user_id:
            print("Cannot view account page, you must be logged in")
            self.redirect('/account/signin')

        session = DbSessionFactory.create_session()
        season_row = session.query(SeasonInfo.current_season).filter(SeasonInfo.id == '1').first()
        season = season_row.current_season

        session.close()

        return {'season': season}

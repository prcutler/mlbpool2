import pyramid_handlers
from mlbpool.controllers.base_controller import BaseController
from mlbpool.viewmodels.newinstallviewmodel import NewInstallViewModel
from mlbpool.viewmodels.newseasonviewmodel import NewSeasonViewModel
from mlbpool.viewmodels.update_mlbplayers_viewmodel import UpdateMLBPlayersViewModel
from mlbpool.services.new_install_service import NewInstallService
from mlbpool.services.new_season_service import NewSeasonService
from mlbpool.services.activeplayers_service import ActivePlayersService
from mlbpool.data.account import Account
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.services.admin_service import AccountService
from mlbpool.viewmodels.update_weekly_stats_viewmodel import UpdateWeeklyStats
from mlbpool.services.weekly_msf_data import WeeklyStatsService
from mlbpool.viewmodels.update_unique_picks_viewmodel import UniquePicksViewModel
from mlbpool.services.unique_picks_service import UniquePicksService
from mlbpool.services.standings_service import StandingsService
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.services.gameday_service import GameDayService
import pendulum
from dateutil import parser


class AdminController(BaseController):
    @pyramid_handlers.action(renderer='templates/admin/index.pt')
    def index(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        session = DbSessionFactory.create_session()

        get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        first_name = get_first_name[0]

        season_info = session.query(SeasonInfo).all()
        season_start_query = session.query(SeasonInfo.season_start_date).first()

        # season_start_query is returned as a tuple and need to get the first part of the tuple:
        season_opener_date = str(season_start_query[0])
        print(season_opener_date)

        # Set the timezone we will be working with
        tz = pendulum.timezone('America/New_York')

        # Convert the start date to a string that Pendulum can work with
        season_start_date_convert = \
            pendulum.from_format(season_opener_date, '%Y-%m-%d %H:%M:%S', tz).to_datetime_string()
        print(season_start_date_convert)

        # Use the string above in a Pendulum instance and get the time deltas needed
        season_start_date = pendulum.parse(season_start_date_convert)

        now = pendulum.now(tz=tz)
        print(now)
        delta = season_start_date - now
        days = delta.days
        hours = delta.hours
        minutes = delta.minutes

        picks_due = season_start_date.to_formatted_date_string()
        time_due = season_start_date.format('%I:%M %p')

#        days = GameDayService.get_season_opener_time(get_days)
#        hours = GameDayService.get_season_opener_time(get_hours)
#        minutes = GameDayService.get_season_opener_time(get_minutes)

        return {'picks_due': picks_due, 'time_due': time_due, 'days': days, 'hours': hours, 'minutes': minutes,
                'first_name': first_name, 'season_info': season_info}

    # GET /admin/new_install
    @pyramid_handlers.action(renderer='templates/admin/new_install.pt',
                             request_method='GET',
                             name='new_install')
    def new_install_get(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = NewInstallViewModel()
        return vm.to_dict()

    # POST /admin/new_install
    @pyramid_handlers.action(renderer='templates/admin/new_install.pt',
                             request_method='POST',
                             name='new_install')
    def new_install_post(self):
        vm = NewInstallViewModel()
        vm.from_dict(self.request.POST)

        # Insert team info
        NewInstallService.get_team_info()
        NewInstallService.create_division_info()
        NewInstallService.create_league_info()
        NewInstallService.create_pick_types()
        NewInstallService.create_pick_type_points()

        # redirect
        self.redirect('/admin/new_season')

    @pyramid_handlers.action(renderer='templates/admin/new_season.pt',
                             request_method='GET',
                             name='new_season')
    def new_season_get(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = NewSeasonViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/new_season.pt',
                             request_method='POST',
                             name='new_season')
    def new_season_post(self):
        vm = NewSeasonViewModel()
        vm.from_dict(self.request.POST)

        # Insert the new season information
        new_season_input = NewSeasonService.create_season(vm.new_season_input, vm.season_all_star_game_date_input)

        # redirect
        self.redirect('/admin/update_mlbplayers')

    @pyramid_handlers.action(renderer='templates/admin/update_mlbplayers.pt',
                             request_method='GET',
                             name='update_mlbplayers')
    def update_mlb_players(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UpdateMLBPlayersViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update_mlbplayers.pt',
                             request_method='POST',
                             name='update_mlbplayers')
    def update_mlb_players_post(self):
        vm = UpdateMLBPlayersViewModel()
        vm.from_dict(self.request.POST)

        # Insert MLBPlayer info
        active_players = ActivePlayersService.add_active_mlbplayers(vm.firstname, vm.lastname, vm.player_id,
                                                                    vm.team_id, vm.position, vm.season)

        # redirect
        self.redirect('/admin/')

    @pyramid_handlers.action(renderer='templates/admin/account-list.pt',
                             request_method='GET',
                             name='account-list')
    def list_accounts(self):

        # Show list of accounts
        account_list = AccountService.get_all_accounts()

        return {'account_list': account_list}

    @pyramid_handlers.action(renderer='templates/admin/update-weekly-stats.pt',
                             request_method='GET',
                             name='update-weekly-stats')
    def update_weekly_stats(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UpdateWeeklyStats()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update-weekly-stats.pt',
                             request_method='POST',
                             name='update-weekly-stats')
    def update_weekly_stats_post(self):
        vm = UpdateWeeklyStats()
        vm.from_dict(self.request.POST)

        # Insert weekly team and player stats
        WeeklyStatsService.get_qb_stats()
        WeeklyStatsService.get_rb_stats()
        WeeklyStatsService.get_rec_stats()
        WeeklyStatsService.get_sack_stats()
        WeeklyStatsService.get_interception_stats()
        WeeklyStatsService.get_team_rankings()
        WeeklyStatsService.get_conference_standings()
        WeeklyStatsService.get_points_for()
        WeeklyStatsService.get_tiebreaker()
        StandingsService.update_player_pick_points()
        StandingsService.update_team_pick_points()

        # redirect
        self.redirect('/admin')

    @pyramid_handlers.action(renderer='templates/admin/update-unique-picks.pt',
                             request_method='GET',
                             name='update-unique-picks')
    def update_unique_picks(self):
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UniquePicksViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update-unique-picks.pt',
                             request_method='POST',
                             name='update-unique-picks')
    def update_unique_picks_post(self):
        vm = UniquePicksViewModel()
        vm.from_dict(self.request.POST)

        # Find all unique picks for each player
        # team type picks
        picktype = 1
        conf = 0
        div = 1

        while conf < 2:
            rank = 1
            UniquePicksService.unique_team_picks(picktype, conf, div, rank)
            rank = 2
            UniquePicksService.unique_team_picks(picktype, conf, div, rank)
            rank = 4
            UniquePicksService.unique_team_picks(picktype, conf, div, rank)
            div += 1
            if div > 4:
                div = 1
                conf += 1

        picktype = 9
        conf = 0
        UniquePicksService.unique_team_picks(picktype, conf)
        conf = 1
        UniquePicksService.unique_team_picks(picktype, conf)

        picktype = 10
        UniquePicksService.unique_team_picks(picktype)

        picktype = 4
        conf = 0
        while picktype < 9:
            UniquePicksService.unique_player_picks(picktype, conf)
            conf += 1
            if conf > 1:
                picktype += 1
                conf = 0

        # redirect
        self.redirect('/admin')

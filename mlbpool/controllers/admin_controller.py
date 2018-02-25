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


class AdminController(BaseController):
    @pyramid_handlers.action(renderer='templates/admin/index.pt')
    def index(self):
        """GET request for the admin homepage.  If the database is empty, redirect to new_install"""
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        get_first_name = session.query(Account.first_name).filter(Account.id == self.logged_in_user_id) \
            .first()
        first_name = get_first_name[0]

        season_info = session.query(SeasonInfo).all()
        print(season_info)

        if GameDayService.admin_check() is None:
            self.redirect('/admin/new_install')

        else:

            season_start_date = GameDayService.season_opener_date()
            picks_due = GameDayService.picks_due()
            time_due = GameDayService.time_due()

            now_time = pendulum.now(tz=pendulum.timezone('America/New_York')).to_datetime_string()

            # Use the string above in a Pendulum instance and get the time deltas needed
            now_time = pendulum.parse(now_time)

            delta = season_start_date - now_time
            days = delta.days
            hours = delta.hours
            minutes = delta.minutes

            return {'picks_due': picks_due, 'time_due': time_due, 'days': days, 'hours': hours, 'minutes': minutes,
                    'first_name': first_name, 'season_info': season_info}

    # GET /admin/new_install
    @pyramid_handlers.action(renderer='templates/admin/new_install.pt',
                             request_method='GET',
                             name='new_install')
    def new_install_get(self):
        """For first time installation, create the team, division, league, pick_types and points tables"""
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
        """For first time installation, create the team, division, league, pick_types and points tables"""
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
        """Update the year to a new season"""
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
        """Update the year to a new season"""
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
        """After updating to a new season, get a list of all MLB playes for that season"""
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        session.close()

        vm = UpdateMLBPlayersViewModel()
        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update_mlbplayers.pt',
                             request_method='POST',
                             name='update_mlbplayers')
    def update_mlb_players_post(self):
        """After updating to a new season, get a list of all MLB playes for that season"""
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
        """Show list of accounts"""
        account_list = AccountService.get_all_accounts()

        return {'account_list': account_list}

    @pyramid_handlers.action(renderer='templates/admin/update-weekly-stats.pt',
                             request_method='GET',
                             name='update-weekly-stats')
    def update_weekly_stats(self):
        """Update the stats"""
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UpdateWeeklyStats()

        session.close()

        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update-weekly-stats.pt',
                             request_method='POST',
                             name='update-weekly-stats')
    def update_weekly_stats_post(self):
        """Call all the mthods to update all stats in the database"""
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
        """Right after the season starts and right after the All-Star Break when pick changes are complete,
        run this to see what picks are unique for each pool player"""
        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        vm = UniquePicksViewModel()

        session.close()

        return vm.to_dict()

    @pyramid_handlers.action(renderer='templates/admin/update-unique-picks.pt',
                             request_method='POST',
                             name='update-unique-picks')
    def update_unique_picks_post(self):
        """Right after the season starts and right after the All-Star Break when pick changes are complete,
                run this to see what picks are unique for each pool player"""
        vm = UniquePicksViewModel()
        vm.from_dict(self.request.POST)

        # Find all unique picks for each player
        # team type picks
        picktype = 1
        league = 0
        div = 1

        # TODO The division numbers have changed from NFLPool to MLBPool (4 to 3) and rank is 5

        while league < 2:
            rank = 1
            UniquePicksService.unique_team_picks(picktype, league, div, rank)

            rank = 2
            UniquePicksService.unique_team_picks(picktype, league, div, rank)

            rank = 4
            UniquePicksService.unique_team_picks(picktype, league, div, rank)

            div += 1

            if div > 4:
                div = 1
                league += 1

        picktype = 9
        league = 0
        UniquePicksService.unique_team_picks(picktype, league)

        league = 1
        UniquePicksService.unique_team_picks(picktype, league)

        picktype = 10
        UniquePicksService.unique_team_picks(picktype)

        picktype = 4
        league = 0

        while picktype < 9:
            UniquePicksService.unique_player_picks(picktype, league)
            league += 1
            if league > 1:
                picktype += 1
                league = 0

        # redirect
        self.redirect('/admin')

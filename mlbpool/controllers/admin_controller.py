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
from mlbpool.viewmodels.trades_viewmodel import TradesViewModel
from mlbpool.services.unique_picks_service import UniquePicksService
from mlbpool.services.standings_service import StandingsService
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.services.gameday_service import GameDayService
from mlbpool.services.time_service import TimeService
from mlbpool.services.trade_service import TradeService
from mlbpool.viewmodels.admin_update_viewmodel import AdminViewModel


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

        if GameDayService.admin_check() is None:
            self.redirect('/admin/new_install')

        else:

            season_start_date = GameDayService.season_opener_date()
            picks_due = GameDayService.picks_due()
            time_due = GameDayService.time_due()

            # Use the string above in a Pendulum instance and get the time deltas needed
            now_time = TimeService.get_time()

            days = GameDayService.delta_days()
            hours = GameDayService.delta_hours()
            minutes = GameDayService.delta_minutes()

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
        """After updating to a new season, get a list of all MLB players for that season"""
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
        """After updating to a new season, get a list of all MLB players for that season"""
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

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        account_list = AccountService.get_all_accounts()

        session.close()

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
        """Call all the methods to update all stats in the database"""
        vm = UpdateWeeklyStats()
        vm.from_dict(self.request.POST)

        # Insert weekly team and player stats
        WeeklyStatsService.get_hitter_stats()
        WeeklyStatsService.get_pitcher_stats()
        WeeklyStatsService.get_team_rankings()
        WeeklyStatsService.get_league_standings()
        WeeklyStatsService.get_tiebreaker()

        WeeklyStatsService.trade_adjustments()
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

    @pyramid_handlers.action(renderer='templates/admin/pitcher-trades.pt',
                             request_method='GET',
                             name='pitcher-trades')
    def pitcher_trades(self):
        """Move a player from one league to another when traded during the season and create split stats."""
        vm = TradesViewModel()

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        pitchers = TradeService.pitcher_list()
        teams = TradeService.team_list()

        session.close()

        return {'pitchers': pitchers, 'teams': teams}

    @pyramid_handlers.action(renderer='templates/admin/pitcher-trades',
                             request_method='POST',
                             name='pitcher-trades')
    def pitcher_trades_post(self):
        """POST request to update the database with the trade information to create the player split."""
        vm = TradesViewModel()
        vm.from_dict(self.request.POST)

        pitcher_trade = TradeService.get_pitcher_trade(vm.player_id, vm.team_id,
                                                       vm.games, vm.p_wins, vm.era, vm.er, vm.ip)

        # redirect
        self.redirect('/admin')

    @pyramid_handlers.action(renderer='templates/admin/hitter-trades.pt',
                             request_method='GET',
                             name='hitter-trades')
    def hitter_trades(self):
        """Move a player from one league to another when traded during the season and create split stats."""
        vm = TradesViewModel()

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        hitters = TradeService.hitter_list()
        teams = TradeService.team_list()

        session.close()

        return {'hitters': hitters, 'teams': teams}

    @pyramid_handlers.action(renderer='templates/admin/hitter-trades',
                             request_method='POST',
                             name='hitter-trades')
    def hitter_trades_post(self):
        """POST request to update the database with the trade information to create the player split."""
        vm = TradesViewModel()
        vm.from_dict(self.request.POST)

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        hitter_trade = TradeService.get_hitter_trade(vm.player_id, vm.team_id,
                                                     vm.hr, vm.ba, vm.ab, vm.hits, vm.pa, vm.games, vm.rbi)

        session.close()

        # redirect
        self.redirect('/admin')

    @pyramid_handlers.action(renderer='templates/admin/update-admin.pt',
                             request_method='GET',
                             name='update-admin')
    def make_admin(self):
        """Move a player from one league to another when traded during the season and create split stats."""
        vm = AdminViewModel()

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        pool_player_list = AccountService.get_all_accounts()

        session.close()

        return {'players': pool_player_list}

    @pyramid_handlers.action(renderer='templates/admin/update-admin',
                             request_method='POST',
                             name='update-admin')
    def update_admin(self):
        """POST request to update the database with the trade information to create the player split."""
        vm = AdminViewModel()
        vm.from_dict(self.request.POST)

        session = DbSessionFactory.create_session()
        su__query = session.query(Account.id).filter(Account.is_super_user == 1)\
            .filter(Account.id == self.logged_in_user_id).first()

        if su__query is None:
            print("You must be an administrator to view this page")
            self.redirect('/home')

        update_admin = AccountService.update_admin(vm.new_admin)

        session.close()

        # redirect
        self.redirect('/admin')
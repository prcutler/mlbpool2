import pyramid_handlers
from mlbpool.controllers.base_controller import BaseController
from mlbpool.viewmodels.standings_viewmodel import StandingsViewModel
from mlbpool.services.standings_service import StandingsService
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.weekly_player_results import WeeklyPlayerResults
from mlbpool.viewmodels.standings_season_points_viewmodel import StandingsPointsViewModel
from mlbpool.services.gameday_service import GameDayService
from mlbpool.services.time_service import TimeService
import pendulum


class StandingsController(BaseController):
    @pyramid_handlers.action(renderer='templates/standings/standings.pt')
    def index(self):
        """Get a list of all seasons played from the database and display a bulleted list for the user to
        choose which season to view standings for"""
        seasons_played = StandingsService.all_seasons_played()

        return {'seasons': seasons_played}

    @pyramid_handlers.action(renderer='templates/standings/season.pt',
                             request_method='GET',
                             name='season')
    def season(self):
        """View the standings for a given season from the user choosing in the bullet list in index"""
        vm = StandingsPointsViewModel()
        vm.from_dict(self.data_dict)

        season = self.request.matchdict['id']
        season_year = pendulum.parse(season)

        current_standings = StandingsService.display_weekly_standings(season)

        session = DbSessionFactory.create_session()

        date_query = session.query(WeeklyPlayerResults.update_date)\
            .order_by(WeeklyPlayerResults.update_date.desc()).first()

        if date_query is None:
            self.redirect('/home')

        else:

            if TimeService.get_time() > GameDayService.last_game_date():
                date_updated = 'Final Standings'

            else:
                date_updated = date_query[0]

            return {'current_standings': current_standings, 'season': season, 'date_updated': date_updated}

        session.close()

    @pyramid_handlers.action(renderer='templates/standings/player-standings.pt',
                             request_method='GET',
                             name='player-standings')
    def player_standings_get(self):
        vm = StandingsViewModel()
        vm.from_dict(self.data_dict)

        player = self.request.matchdict['id']

        player_standings = StandingsService.display_player_standings(player)

        first_name = (player_standings[0]['first_name'])
        last_name = (player_standings[0]['last_name'])

        return {'first_name': first_name, 'last_name': last_name, 'player_standings': player_standings}

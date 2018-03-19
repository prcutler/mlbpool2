import pendulum
from mlbpool.data.seasoninfo import SeasonInfo
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.services.time_service import TimeService


# Set the timezone we will be working with
timezone = pendulum.timezone('America/New_York')

# Change now_time for testing
# Use this one for production:
# now_time = pendulum.now(tz=pendulum.timezone('America/New_York'))
# Use this one for testing:
now_time = TimeService.get_time()


def season_opener():

    session = DbSessionFactory.create_session()

    season_start_query = session.query(SeasonInfo.season_start_date).first()
    # print("Season Start Query:", season_start_query)

    # season_start_query is returned as a tuple and need to get the first part of the tuple:
    season_opener_date = str(season_start_query[0])

    # Convert the start date to a string that Pendulum can work with
    # season_start_date_convert = \
    #    pendulum.from_format(season_opener_date, '%Y-%m-%d %H:%M:%S', timezone).to_datetime_string()

    # Use the string above in a Pendulum instance and get the time deltas needed
    season_start_date = pendulum.parse(season_opener_date)

    session.close()

    return season_start_date


class GameDayService:
    @staticmethod
    def admin_check():
        session = DbSessionFactory.create_session()

        season_start_query = session.query(SeasonInfo.season_start_date).first()

        session.close()

        return season_start_query

    @staticmethod
    def season_opener_date():
        """Get the time of the season opener's game"""

        season_opener_date = season_opener()

        return season_opener_date

    @staticmethod
    def all_star_game_date():
        """Get the time of the season opener's game"""
        session = DbSessionFactory.create_session()

        all_star_game_date = session.query(SeasonInfo.all_star_game_date).first()

        session.close()

        return all_star_game_date

    @staticmethod
    def last_game_date():
        session = DbSessionFactory.create_session()

        last_game_date = session.query(SeasonInfo.season_end_date).first()
        last_game_info = str(last_game_date[0])
        last_game = pendulum.parse(last_game_info)
        print(last_game)

        session.close()

        return last_game

    @staticmethod
    def timezone():
        tz = pendulum.timezone('America/New_York')

        return tz

    @staticmethod
    def time_due():
        season_start_date = season_opener()
        time_due = season_start_date.format('%I:%M %p')
        # print("Season start date", season_start_date, "time_due", time_due)

        return time_due

    @staticmethod
    def picks_due():
        season_start_date = season_opener()
        picks_due_date = season_start_date.to_formatted_date_string()
        # print("picks_due_date", picks_due_date)

        return picks_due_date

    @staticmethod
    def delta_days():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        days = delta.days

        return days

    @staticmethod
    def delta_hours():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        hours = delta.hours

        return hours

    @staticmethod
    def delta_minutes():

        season_start_date = season_opener()
        now = now_time

        delta = season_start_date - now
        minutes = delta.minutes

        return minutes

    @staticmethod
    def all_star_break(all_star_break_date):
        """Get the date of the All Star Game from the database and create the window when a user can change picks"""

        # Get the All-Star break info from the database
        session = DbSessionFactory.create_session()
        all_star_game_query = session.query(SeasonInfo.all_star_game_date).first()
        all_star_game_date = str(all_star_game_query[0])
        start_time = (all_star_game_date + " 19:00")
        all_star_game = pendulum.from_format(start_time, '%Y-%m-%d %H:%M', tz=timezone)

        season_start_date = season_opener()

        print("Converted:", all_star_game)
        print("Now time:", all_star_break_date)

        all_star_game_break_start = all_star_game.subtract(hours=48)
        print("Break starts at", all_star_game_break_start)
        all_star_break_end = (all_star_game.add(hours=48))
        print("Break ends at", all_star_break_end)

        session.close()

        if all_star_break_date > all_star_break_end:
            print("The current date is greater than the when the break ends")
            return False

        elif all_star_break_date < season_start_date:

            return True

        elif all_star_game_break_start < all_star_break_date < all_star_break_end:

            return True

        elif all_star_break_date < all_star_game_break_start:
            print("The current date is less than the start of the all-star break")
            return False

        else:
            print(False)
            return False

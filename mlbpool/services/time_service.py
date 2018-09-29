import pendulum
import pymysql

# Needed for pymysql to understand Pendulum datetimes
pymysql.converters.conversions[pendulum.DateTime] = pymysql.converters.escape_datetime


class TimeService:
    @staticmethod
    def get_time():
        """Create a service to get the time - there were too many instances of getting the current time in
        the codebase making testing difficult."""
        # Change now_time for testing
        # Use this one for production:
        # now_time = pendulum.now(tz=pendulum.timezone('America/New_York')).to_datetime_string()
        now_time = pendulum.now(tz=pendulum.timezone("America/New_York"))
        # Use this one for testing:
        # now_time = pendulum.datetime(2018, 3, 28, 12, 00, tz='America/New_York')

        return now_time

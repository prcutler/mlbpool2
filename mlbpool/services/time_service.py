import pendulum
from pendulum import Pendulum
import pymysql

# Needed for pymysql to understand Pendulum datetimes
pymysql.converters.conversions[Pendulum] = pymysql.converters.escape_datetime


class TimeService:
    @staticmethod
    def get_time():
        """Create a service to get the time - there were too many instances of getting the current time in
        the codebase making testing difficult."""
        # Change now_time for testing
        # Use this one for production:
        # now_time = pendulum.now(tz=pendulum.timezone('America/New_York')).to_datetime_string()
        # Use this one for testing:
        now_time = pendulum.create(2017, 7, 14, 13, 00, tz='America/New_York')
        #now_time = pendulum.create(2017, 4, 11, 13, 00, tz='America/New_York')

        return now_time

import pendulum


class TimeService:
    @staticmethod
    def get_time(self):
        """Create a service to get the time - there were too many instances of getting the current time in
        the codebase making testing difficult."""
        # Change now_time for testing
        # Use this one for production:
        # now_time = pendulum.now(tz=pendulum.timezone('America/New_York')).to_datetime_string()
        # Use this one for testing:
        now_time = pendulum.create(2017, 3, 17, 18, 59, tz='America/New_York')

        return now_time

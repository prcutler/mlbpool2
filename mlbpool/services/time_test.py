import pendulum
from dateutil import parser
import datetime

date = "2018-03-29"
time = "12:40PM"
dt = (2018, 3, 29, 12, 40)

tz = "America/New_York"

# season_start_dt = date + "T" + time[:-2]
season_start_dt = str(dt)

season = pendulum.from_timestamp(season_start_dt).to_datetime_string()

now = pendulum.now(tz=tz)

# print(pendulum.parse(season_start_dt))

print(now)
print(season_start_dt)

# dt_test = parser.parse(season_start_dt)
# print(dt_test)

delta = season_start_dt - now
print(delta.days, "days", delta.hours, "hours and", delta.minutes, "minutes")


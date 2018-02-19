import pendulum
from dateutil import parser

date = "2018-03-29"
time = "12:40PM"

tz = "America/New_York"

season_start_dt = date + "T" + time[:-2]
now = pendulum.now(tz=tz)

# print(pendulum.parse(season_start_dt))

print(now)
print(season_start_dt)

dt_test = parser.parse(season_start_dt)
print(dt_test)

delta = dt_test - now
print(delta.days, "days", delta.hours, "hours and", delta.minutes, "minutes")


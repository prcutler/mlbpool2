from mlbpool.data.teaminfo import TeamInfo
import requests
import mlbpool.data.config as secret
from requests.auth import HTTPBasicAuth
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.picktypes import PickTypes
from mlbpool.data.pick_type_points import PickTypePoints


class NewInstallService:

    @staticmethod
    def get_install():
        return []

    @staticmethod
    def get_team_info():
        """From MySportsFeeds get the team name, team city, team ID and abbreviation.  Loop through
        the AFC teams (0 in the API) and NFC (1) in the API.  The Division IDs are self created.  This method
        will fill the TeamInfo table in the database."""

        session = DbSessionFactory.create_session()

        x = 0
        y = 0

        response = requests.get(
            'https://api.mysportsfeeds.com/v1.2/pull/mlb/2018-regular/conference_team_standings.json',
            auth=HTTPBasicAuth(secret.msf_username, secret.msf_pw))

        data = response.json()

        teamlist = data["conferenceteamstandings"]["conference"][0]["teamentry"]

        # Create a loop to extract each team name (American League first, then National League)

        for al_team_list in teamlist:
            al_team_name = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["Name"]
            al_team_city = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["City"]
            al_team_id = int(data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["ID"])
            al_team_abbr = data["conferenceteamstandings"]["conference"][0]["teamentry"][x]["team"]["Abbreviation"]

            if al_team_id <= 115:
                division_id = 1
            elif al_team_id <= 120:
                division_id = 2
            else:
                division_id = 3

            x = x + 1

            team_info = TeamInfo(city=al_team_city, team_id=al_team_id, team_abbr=al_team_abbr,
                                 name=al_team_name, league_id=0, division_id=division_id)

            session.add(team_info)

            session.commit()

        for nl_team_list in teamlist:
            nl_team_name = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["Name"]
            nl_team_city = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["City"]
            nl_team_id = int(data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["ID"])
            nl_team_abbr = data["conferenceteamstandings"]["conference"][1]["teamentry"][y]["team"]["Abbreviation"]

            if nl_team_id <= 130:
                division_id = 1
            elif nl_team_id <= 135:
                division_id = 2
            else:
                division_id = 3

            y = y + 1

            team_info = TeamInfo(city=nl_team_city, team_id=nl_team_id, team_abbr=nl_team_abbr,
                                 name=nl_team_name, league_id=1, division_id=division_id)

            session.add(team_info)

            session.commit()

    @classmethod
    def create_division_info(cls):
        """Create the DivisionInfo table with the division IDs and name them to match MLB division names."""
        for x in range(1, 4):
            division_id = x
            if x == 1:
                division = 'East'
            elif x == 2:
                division = 'Central'
            else:
                division = 'West'

            session = DbSessionFactory.create_session()

            division_info = DivisionInfo(division=division, division_id=division_id)

            session.add(division_info)
            session.commit()

    @classmethod
    def create_league_info(cls):
        """Fill out the needed data in the LeagueInfo table"""
        for x in range(1, 3):
            if x == 1:
                league_id = 0
                league = 'AL'
            else:
                league_id = 1
                league = 'NL'

            session = DbSessionFactory.create_session()

            league_info = LeagueInfo(league=league, league_id=league_id)

            session.add(league_info)
            session.commit()

    @classmethod
    def create_pick_types(cls):
        """Create the pick types used for when a user submits picks, displays their picks and for calculating
            player scores.  Type 2 not used at this time, instead player stats have their own type
            (home runs, batting average, pitcher wins, etc.)"""
        for x in range(1, 11):
            if x == 1:
                name = 'team'
            elif x == 2:
                name = 'unused'
            elif x == 3:
                name = 'team_wins'
            elif x == 4:
                name = "home_runs"
            elif x == 5:
                name = "batting_average"
            elif x == 6:
                name = "RBI"
            elif x == 7:
                name = "pitcher_wins"
            elif x == 8:
                name = "ERA"
            elif x == 9:
                name = "wildcard"
            else:
                name = 'tiebreaker'

            session = DbSessionFactory.create_session()

            pick_type_info = PickTypes(name=name)
            session.add(pick_type_info)
            session.commit()

    @staticmethod
    def create_pick_type_points():
        """Assign how many points each different kind of pick is worth"""
        for x in range(1, 11):
            """Assign the value of team standings picks"""
            pick_type_id = x
            if x == 1:
                for y in range(1, 6):
                    # TODO Check this range
                    rank = y

                    if y == 1:
                        points = 50
                    elif y == 2:
                        points = 30
                    elif y == 5:
                        points = 20
                    else:
                        points = 0

                    if points != 0:
                        session = DbSessionFactory.create_session()
                        pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                        session.add(pick_type_points)
                        session.commit()

            elif x == 2:
                continue

            elif x == 3:

                # TODO Check with Kelly that this is correct

                rank = 1
                points = 10

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)
                session.commit()

                rank = 15
                points = 10

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)
                session.commit()

            elif 3 < x < 9:
                """Assign the value of individual MLB player picks such as home runs or pitcher wins"""

                for y in range(1, 4):
                    rank = y
                    if y == 1:
                        points = 30
                    elif y == 2:
                        points = 20
                    else:
                        points = 10

                    session = DbSessionFactory.create_session()

                    pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                    session.add(pick_type_points)
                    session.commit()

            elif x == 9:
                """Assign the points value for the wildcard picks for each league"""
                for y in range(1, 3):
                    rank = y
                    points = 10

                    session = DbSessionFactory.create_session()

                    pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                    session.add(pick_type_points)
                    session.commit()

            else:
                """Assign the Twins wins tiebreaker points value"""
                rank = 1
                points = 1000
                session = DbSessionFactory.create_session()

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)
                session.commit()


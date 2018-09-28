from mlbpool.data.teaminfo import TeamInfo
import requests
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth
from mlbpool.data.dbsession import DbSessionFactory
from mlbpool.data.divisioninfo import DivisionInfo
from mlbpool.data.leagueinfo import LeagueInfo
from mlbpool.data.picktypes import PickTypes
from mlbpool.data.pick_type_points import PickTypePoints
from mlbpool.data.seasoninfo import SeasonInfo


class NewInstallService:

    @staticmethod
    def get_install():
        return []

    @staticmethod
    def get_team_info():
        """From MySportsFeeds get the team name, team city, team ID and abbreviation.  Loop through
        all teams in the API.  The Division IDs are self created.  This method
        will fill the TeamInfo table in the database."""

        session = DbSessionFactory.create_session()
        season_query = session.query(SeasonInfo.current_season).first()
        season = season_query[0]

        x = 0

        response = requests.get(
            'https://api.mysportsfeeds.com/v2.0/pull/mlb/' + str(season) + '-regular/standings.json',
            auth=HTTPBasicAuth(config.msf_api, config.msf_v2pw))

        data = response.json()

        teamlist = data["teams"]

        # Create a loop to extract each team name (American League first, then National League)

        for team_list in teamlist:
            team_name = teamlist[x]["team"]["name"]
            team_city = teamlist[x]["team"]["city"]
            team_id = int(teamlist[x]["team"]["id"])
            team_abbr = teamlist[x]["team"]["abbreviation"]
            conference_name = teamlist[x]["conferenceRank"]["conferenceName"]
            division_name = teamlist[x]["divisionRank"]["divisionName"]

            if division_name == 'East':
                division_id = 1
            elif division_name == 'Central':
                division_id = 2
            else:
                division_id = 3

            if conference_name == 'American League':
                league_id = 0
            else:
                league_id = 1

            x += 1

            team_info = TeamInfo(city=team_city, team_id=team_id, team_abbr=team_abbr,
                                 name=team_name, league_id=league_id, division_id=division_id)

            session.add(team_info)

            session.commit()

        session.close()

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

            session.close()

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

            session.close()

    @classmethod
    def create_pick_types(cls):
        """Create the pick types used for when a user submits picks, displays their picks and for calculating
            player scores.  Type 2 not used at this time, instead player stats have their own type
            (home runs, batting average, pitcher wins, etc.)"""
        for x in range(1, 11):
            if x == 1:
                name = 'team'
            elif x == 2:
                name = 'team_losses'
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

            session.close()

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
                        session.close()

            elif x == 2:
                """For pick type 2, assign to 1 team in each league who has the most losses.  Out of the 15 teams
                in each league, their rank would be 15th and assign rank == 15."""

                rank = 15
                points = 20

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)

                session.commit()
                session.close()

            elif x == 3:
                """For pick type 3, assign to 1 team in each league who has the most wins.  Out of the 15 teams
                in each league, their rank would be 1st and assign rank == 1."""

                rank = 1
                points = 20

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)

                session.commit()
                session.close()

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
                    session.close()

            elif x == 9:
                """Assign the points value for the wildcard picks for each league"""
                for y in range(1, 3):
                    rank = y
                    points = 10

                    session = DbSessionFactory.create_session()

                    pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                    session.add(pick_type_points)

                    session.commit()
                    session.close()

            else:
                """Assign the Twins wins tiebreaker points value"""
                rank = 1
                points = 1000
                session = DbSessionFactory.create_session()

                pick_type_points = PickTypePoints(pick_type_id=pick_type_id, rank=rank, points=points)
                session.add(pick_type_points)

                session.commit()
                session.close()


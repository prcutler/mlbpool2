import pytest
import requests
import mlbpool.data.config as config
from requests.auth import HTTPBasicAuth


def test_get_hitter_stats_api():

    msf_hitter_api = requests.get('https://api.mysportsfeeds.com/v1.2/pull/mlb/2017-regular/'
                                  'cumulative_player_stats.json?playerstats=HR,AVG,RBI,PA,H,AB'
                                  '&position=C,1B,2B,SS,3B,OF,RF,CF,LF,DH',
                                  auth=HTTPBasicAuth(config.msf_username, config.msf_pw))

    status = msf_hitter_api.status_code

    return status


def test_msf_hitter_api_answer():

    assert test_get_hitter_stats_api() == 200

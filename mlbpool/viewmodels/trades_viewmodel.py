from mlbpool.viewmodels.viewmodelbase import ViewModelBase


class TradesViewModel(ViewModelBase):
    def __init__(self):
        self.firstname = None
        self.lastname = None
        self.player_id = None
        self.team_id = None
        self.position = None
        self.season = None
        self.hr = None
        self.ba = None
        self.ab = None
        self.hits = None
        self.pa = None
        self.games = None
        self.rbi = None
        self.p_wins = None
        self.era = None
        self.er = None
        self.ip = None

    def from_dict(self, data_dict):
        self.firstname = data_dict.get("firstname")
        self.lastname = data_dict.get("lastname")
        self.player_id = data_dict.get("player_id")
        self.team_id = data_dict.get("team_id")
        self.position = data_dict.get("position")
        self.season = data_dict.get("season")
        self.hr = data_dict.get("hr")
        self.ba = data_dict.get("ba")
        self.ab = data_dict.get("ab")
        self.hits = data_dict.get("hits")
        self.pa = data_dict.get("pa")
        self.games = data_dict.get("games")
        self.rbi = data_dict.get("rbi")
        self.p_wins = data_dict.get("p_wins")
        self.era = data_dict.get("era")
        self.er = data_dict.get("er")
        self.ip = data_dict.get("ip")

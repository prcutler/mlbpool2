from mlbpool.viewmodels.viewmodelbase import ViewModelBase


class PlayerPicksViewModel(ViewModelBase):
    def __init__(self):
        self.al_east_winner_pick = None
        self.al_east_second = None
        self.al_east_last = None


    def from_dict(self, data_dict):
        self.al_east_winner_pick = data_dict.get('al_east_winner_pick')
        self.al_east_second = data_dict.get('al_east_second')
        self.al_east_last = data_dict.get('al_east_last')




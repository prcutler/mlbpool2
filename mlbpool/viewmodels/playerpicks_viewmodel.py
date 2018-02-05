from mlbpool.viewmodels.viewmodelbase import ViewModelBase


class PlayerPicksViewModel(ViewModelBase):
    def __init__(self):
        self.al_east_winner_pick = None
        self.al_east_second_pick = None
        self.al_east_last_pick = None
        self.al_central_winner_pick = None
        self.al_central_second_pick = None
        self.al_central_last_pick = None
        self.al_west_winner_pick = None
        self.al_west_second_pick = None
        self.al_west_last_pick = None
        self.nl_east_winner_pick = None
        self.nl_east_second_pick = None
        self.nl_east_last_pick = None
        self.nl_central_winner_pick = None
        self.nl_central_second_pick = None
        self.nl_central_last_pick = None
        self.nl_west_winner_pick = None
        self.nl_west_second_pick = None
        self.nl_west_last_pick = None
        self.al_hr_pick = None
        self.nl_hr_pick = None
        self.al_rbi_pick = None
        self.nl_rbi_pick = None
        self.al_ba_pick = None
        self.nl_ba_pick = None
        self.al_p_wins_pick = None
        self.nl_p_wins_pick = None
        self.al_era_pick = None
        self.nl_era_pick = None
        self.al_wildcard1_pick = None
        self.al_wildcard2_pick = None
        self.nl_wildcard1_pick = None
        self.nl_wildcard2_pick = None
        self.al_wins_pick = None
        self.nl_wins_pick = None
        self.al_losses_pick = None
        self.nl_losses_pick = None
        self.twins_wins_pick = None

    def from_dict(self, data_dict):
        self.al_east_winner_pick = data_dict.get('al_east_winner_pick')
        self.al_east_second_pick = data_dict.get('al_east_second_pick')
        self.al_east_last_pick = data_dict.get('al_east_last_pick')
        self.al_central_winner_pick = data_dict.get('al_central_winner_pick')
        self.al_central_second_pick = data_dict.get('al_central_second_pick')
        self.al_central_last_pick = data_dict.get('al_central_last_pick')
        self.al_west_winner_pick = data_dict.get('al_west_winner_pick')
        self.al_west_second_pick = data_dict.get('al_west_second_pick')
        self.al_west_last_pick = data_dict.get('al_west_last_pick')
        self.nl_east_winner_pick = data_dict.get('nl_east_winner_pick')
        self.nl_east_second_pick = data_dict.get('nl_east_second_pick')
        self.nl_east_last_pick = data_dict.get('nl_east_last_pick')
        self.nl_central_winner_pick = data_dict.get('nl_central_winner_pick')
        self.nl_central_second_pick = data_dict.get('nl_central_second_pick')
        self.nl_central_last_pick = data_dict.get('nl_central_last_pick')
        self.nl_west_winner_pick = data_dict.get('nl_west_winner_pick')
        self.nl_west_second_pick = data_dict.get('nl_west_second_pick')
        self.nl_west_last_pick = data_dict.get('nl_west_last_pick')
        self.al_hr_pick = data_dict.get('al_hr_pick')
        self.nl_hr_pick = data_dict.get('nl_hr_pick')
        self.al_rbi_pick = data_dict.get('al_rbi_pick')
        self.nl_rbi_pick = data_dict.get('nl_rbi_pick')
        self.al_ba_pick = data_dict.get('al_ba_pick')
        self.nl_ba_pick = data_dict.get('nl_ba_pick')
        self.al_p_wins_pick = data_dict.get('al_p_wins_pick')
        self.nl_p_wins_pick = data_dict.get('nl_p_wins_pick')
        self.al_era_pick = data_dict.get('al_era_pick')
        self.nl_era_pick = data_dict.get('nl_era_pick')
        self.al_wildcard1_pick = data_dict.get('al_wildcard1_pick')
        self.al_wildcard2_pick = data_dict.get('al_wildcard2_pick')
        self.nl_wildcard1_pick = data_dict.get('nl_wildcard1_pick')
        self.nl_wildcard2_pick = data_dict.get('nl_wildcard2_pick')
        self.al_wins_pick = data_dict.get('al_wins_pick')
        self.nl_wins_pick = data_dict.get('nl_wins_pick')
        self.al_losses_pick = data_dict.get('al_losses_pick')
        self.nl_losses_pick = data_dict.get('nl_losses_pick')
        self.twins_wins_pick = data_dict.get('twins_wins_pick')


